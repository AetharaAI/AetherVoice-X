from __future__ import annotations

import json
import mimetypes
from pathlib import Path

import boto3


class StorageManager:
    def __init__(
        self,
        endpoint: str | None,
        access_key: str | None,
        secret_key: str | None,
        region: str,
        local_root: str,
    ) -> None:
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.local_root = Path(local_root)
        self._client = None

    def _use_s3(self) -> bool:
        return bool(self.endpoint and self.access_key and self.secret_key)

    def _client_or_none(self):
        if not self._use_s3():
            return None
        if self._client is None:
            self._client = boto3.client(
                "s3",
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
        return self._client

    def ensure_bucket(self, bucket: str) -> None:
        client = self._client_or_none()
        if client is None:
            (self.local_root / bucket).mkdir(parents=True, exist_ok=True)
            return
        try:
            client.head_bucket(Bucket=bucket)
        except Exception:
            client.create_bucket(Bucket=bucket)

    def upload_bytes(self, bucket: str, key: str, payload: bytes, content_type: str) -> str:
        client = self._client_or_none()
        if client is None:
            target = self.local_root / bucket / key
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            return target.as_posix()
        client.put_object(Bucket=bucket, Key=key, Body=payload, ContentType=content_type)
        return f"s3://{bucket}/{key}"

    def upload_json(self, bucket: str, key: str, payload: dict) -> str:
        return self.upload_bytes(bucket, key, json.dumps(payload).encode("utf-8"), "application/json")

    def _local_path_for_uri(self, uri: str) -> Path:
        path = Path(uri)
        resolved = path.resolve()
        try:
            resolved.relative_to(self.local_root.resolve())
        except ValueError as exc:
            raise ValueError(f"Artifact path is outside the configured storage root: {uri}") from exc
        return resolved

    def read_bytes(self, uri: str) -> bytes:
        if uri.startswith("s3://"):
            client = self._client_or_none()
            if client is None:
                raise RuntimeError("S3 artifact requested but S3 client is not configured.")
            bucket_and_key = uri[5:]
            bucket, _, key = bucket_and_key.partition("/")
            if not bucket or not key:
                raise ValueError(f"Invalid S3 URI: {uri}")
            response = client.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
        return self._local_path_for_uri(uri).read_bytes()

    def guess_content_type(self, uri: str) -> str:
        content_type, _encoding = mimetypes.guess_type(uri)
        return content_type or "application/octet-stream"
