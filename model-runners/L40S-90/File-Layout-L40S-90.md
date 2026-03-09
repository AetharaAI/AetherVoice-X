ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model$ cd
ubuntu@l40s-90-us-west-or-1:~$ ls- lah
Command 'ls-' not found, did you mean:
  command 'lsd' from snap lsd (0.16.0)
  command 'lsw' from deb suckless-tools (46-1)
  command 'lsh' from deb lsh-client (2.1-13)
  command 'ls' from deb coreutils (8.32-4.1ubuntu1.2)
  command 'lsm' from deb lsm (1.0.4-2)
  command 'lsc' from deb livescript (1.6.1+dfsg-2)
See 'snap info <snapname>' for additional versions.
ubuntu@l40s-90-us-west-or-1:~$ ls -lah
total 152K
drwxr-x--- 12 ubuntu ubuntu 4.0K Mar  9 14:26 .
drwxr-xr-x  4 root   root   4.0K Jan 31 08:50 ..
-rw-------  1 ubuntu ubuntu  47K Mar  9 14:26 .bash_history
-rw-r--r--  1 ubuntu ubuntu  220 Jan  6  2022 .bash_logout
-rw-r--r--  1 ubuntu ubuntu 4.3K Dec 16 09:37 .bashrc
drwx------  5 ubuntu ubuntu 4.0K Dec 16 09:38 .cache
drwxrwxr-x  6 ubuntu ubuntu 4.0K Dec 25 07:22 .config
drwx------  3 ubuntu ubuntu 4.0K Dec  1 05:22 .docker
-rw-------  1 ubuntu ubuntu   20 Mar  4 04:38 .lesshst
drwxrwxr-x  6 ubuntu ubuntu 4.0K Dec 16 09:43 .local
drwx------  3 ubuntu ubuntu 4.0K Dec  1 16:32 .nv
-rw-r--r--  1 ubuntu ubuntu  833 Nov 17 00:07 .profile
drwx------  2 ubuntu ubuntu 4.0K Dec  1 16:25 .ssh
-rw-r--r--  1 ubuntu ubuntu    0 Nov  1 06:22 .sudo_as_admin_successful
-rw-rw-r--  1 ubuntu ubuntu  165 Nov 20 06:49 .wget-hsts
-rw-rw-r--  1 ubuntu ubuntu   26 Nov 17 00:07 .zshrc
drwxrwxr-x  9 ubuntu ubuntu 4.0K Nov 20 08:06 Neuro-Symbiotic
drwxrwxr-x  3 ubuntu ubuntu 4.0K Feb 14 14:42 aether-model-node
drwxr-xr-x  3 ubuntu ubuntu 4.0K Dec  1 16:25 apriel-h1
-rw-rw-r--  1 ubuntu ubuntu  21K Nov 16 16:55 get-docker.sh
drwxrwxr-x 13 ubuntu ubuntu 4.0K Dec  5 10:42 hf-cache
-rw-r--r--  1 root   root   4.0K Feb 10 09:03 old-nginx
ubuntu@l40s-90-us-west-or-1:~$ cd aether-model-node
ubuntu@l40s-90-us-west-or-1:~/aether-model-node$ cd control
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control$ ls -la
total 40
drwxrwxr-x 4 ubuntu ubuntu  4096 Feb 15 23:59 .
drwxrwxr-x 3 ubuntu ubuntu  4096 Feb 14 14:42 ..
-rw-r--r-- 1 root   root     468 Feb 15 23:12 .env
-rw-r--r-- 1 root   root   15820 Feb 15 23:59 config.yaml
-rw-r--r-- 1 root   root     633 Feb 15 23:53 docker-compose.yml
drwxrwxr-x 3 ubuntu ubuntu  4096 Mar  9 15:00 litellm
drwxrwxr-x 9 ubuntu ubuntu  4096 Mar  9 15:18 run-model
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control$ cd litellm
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/litellm$ ls -la
total 48
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  9 15:00 .
drwxrwxr-x 4 ubuntu ubuntu 4096 Feb 15 23:59 ..
-rw-r--r-- 1 root   root    517 Mar  9 14:34 .env
drwxrwxr-x 2 ubuntu ubuntu 4096 Mar  5 10:47 aether-data
-rw-r--r-- 1 root   root   4671 Feb 15 10:54 config.bak
-rw-r--r-- 1 root   root   7118 Mar  9 14:56 config.yaml
-rw-r--r-- 1 root   root   1024 Mar  9 15:00 docker-compose.yml
-rw-r--r-- 1 root   root   7050 Feb 16 02:10 legacy.config.yml
-rw-r--r-- 1 root   root    809 Feb 15 07:35 template-compose.yml
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/litellm$ cd ..
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control$ cd run-model
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model$ ls -la
total 48
drwxrwxr-x 9 ubuntu ubuntu 4096 Mar  9 15:18 .
drwxrwxr-x 4 ubuntu ubuntu 4096 Feb 15 23:59 ..
-rw-r--r-- 1 root   root     90 Feb 15 13:12 .env
drwxr-xr-x 3 root   root   4096 Feb 15 07:54 .mnt
-rw-r--r-- 1 root   root   1731 Feb 15 15:58 docker-compose.yml
-rw-r--r-- 1 root   root   1386 Feb 15 08:10 docker-compose.yml-first
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  9 12:54 dual-qwen
drwxrwxr-x 2 ubuntu ubuntu 4096 Mar  9 12:24 jan-qwen
drwxrwxr-x 2 ubuntu ubuntu 4096 Mar  9 15:20 mini-nan
drwxr-xr-x 3 root   root   4096 Feb 15 07:54 mnt
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  7 12:00 phi4
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  9 12:48 qwen3.5
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model$ cd dual-qwen
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/dual-qwen$ ls -la
total 20
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  9 12:54 .
drwxrwxr-x 9 ubuntu ubuntu 4096 Mar  9 15:18 ..
-rw-r--r-- 1 root   root    145 Mar  9 12:15 Dockerfile.qwen35
-rw-r--r-- 1 root   root   2604 Mar  9 12:53 docker-compose.yml
drwxr-xr-x 4 root   root   4096 Mar  9 12:54 logs
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/dual-qwen$ cd ..
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model$ cd qwen3.5
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/qwen3.5$ cd ..
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model$ cd qwen3.5
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/qwen3.5$ ls -la
total 24
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  9 12:48 .
drwxrwxr-x 9 ubuntu ubuntu 4096 Mar  9 15:18 ..
-rw-r--r-- 1 root   root    145 Mar  5 09:54 Dockerfile.qwen35
-rw-r--r-- 1 root   root   2429 Mar  9 12:48 docker-compose.yml
-rw-r--r-- 1 root   root   2305 Mar  5 09:11 dual-compose.yml
drwxr-xr-x 4 root   root   4096 Mar  5 09:17 logs
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/qwen3.5$ cd ..
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model$ cd mini-nan
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/mini-nan$ ls -la
total 16
drwxrwxr-x 2 ubuntu ubuntu 4096 Mar  9 15:20 .
drwxrwxr-x 9 ubuntu ubuntu 4096 Mar  9 15:18 ..
-rw-r--r-- 1 ubuntu ubuntu   90 Mar  9 15:20 .env
-rw-r--r-- 1 ubuntu ubuntu 1731 Mar  9 15:19 docker-compose.yml
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/run-model/mini-nan$ cd /mnt/aetherpro
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro$ ls -la
total 40
drwxr-xr-x 7 ubuntu ubuntu  4096 Feb 15 08:19 .
drwxr-xr-x 3 root   root    4096 Dec 16 09:10 ..
drwxr-xr-x 3 root   root    4096 Feb 15 08:19 cache
drwxr-xr-x 7 ubuntu ubuntu  4096 Mar  7 07:34 hf
drwxrwxr-x 4 ubuntu ubuntu  4096 Jan 19 05:10 llm
drwx------ 2 ubuntu ubuntu 16384 Dec 16 09:25 lost+found
drwxr-xr-x 7 ubuntu ubuntu  4096 Mar  4 05:13 models
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro$ cd models
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd llm
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/llm$ ls
LFM2.5-1.2B-Thinking  Nanbeige  apriel  april  cyankiwi  mistral
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/llm$ cd cyankiwi
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/llm/cyankiwi$ ls -la
total 12
drwxrwxr-x 3 ubuntu ubuntu 4096 Feb 15 06:49 .
drwxr-xr-x 8 ubuntu ubuntu 4096 Feb 15 12:26 ..
drwxrwxr-x 3 ubuntu ubuntu 4096 Feb 15 06:49 Qwen3-30B-A3B-Thinking-2507-AWQ-4bit
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/llm/cyankiwi$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/llm$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro$ ls
cache  hf  llm  lost+found  models
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro$ cd llm
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/llm$ ls
agent-cpm  qwen3
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/llm$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro$ cd models
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ ls -la
total 28
drwxr-xr-x 7 ubuntu ubuntu 4096 Mar  4 05:13 .
drwxr-xr-x 7 ubuntu ubuntu 4096 Feb 15 08:19 ..
drwxrwxr-x 6 ubuntu ubuntu 4096 Mar  4 05:41 cyankiwi
drwxr-xr-x 8 ubuntu ubuntu 4096 Feb 15 12:26 llm
drwxrwxr-x 6 ubuntu ubuntu 4096 Dec 25 07:24 sensors
drwxr-xr-x 4 ubuntu ubuntu 4096 Feb 14 14:47 vision
drwxr-xr-x 4 ubuntu ubuntu 4096 Mar  7 06:32 voice
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd cyankiwi
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/cyankiwi$ ls -la
total 24
drwxrwxr-x 6 ubuntu ubuntu 4096 Mar  4 05:41 .
drwxr-xr-x 7 ubuntu ubuntu 4096 Mar  4 05:13 ..
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  4 05:35 Jan-code-4b-AWQ-4bit
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  4 05:13 Qwen3.5-35B-A3B-AWQ-4bit
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  4 05:17 Qwen3.5-4B-AWQ-4bit
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  4 05:41 Qwen3.5-9B-AWQ-BF16-INT8
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/cyankiwi$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd sensors
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors$ ls -la
total 24
drwxrwxr-x 6 ubuntu ubuntu 4096 Dec 25 07:24 .
drwxr-xr-x 7 ubuntu ubuntu 4096 Mar  4 05:13 ..
drwxrwxr-x 3 ubuntu ubuntu 4096 Dec 25 07:08 detection
drwxrwxr-x 5 ubuntu ubuntu 4096 Dec 25 07:14 ocr
drwxrwxr-x 5 ubuntu ubuntu 4096 Dec 25 07:15 pose
drwxrwxr-x 5 ubuntu ubuntu 4096 Dec 25 07:15 tracking
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors$ cd detection
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/detection$ ls -la
total 12
drwxrwxr-x 3 ubuntu ubuntu 4096 Dec 25 07:08 .
drwxrwxr-x 6 ubuntu ubuntu 4096 Dec 25 07:24 ..
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:24 yolo
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/detection$ cd yolo
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/detection/yolo$ ls -la
total 51208
drwxrwxr-x 2 ubuntu ubuntu     4096 Dec 25 07:24 .
drwxrwxr-x 3 ubuntu ubuntu     4096 Dec 25 07:08 ..
-rw-rw-r-- 1 ubuntu ubuntu 52425230 Dec 25 07:22 yolov10l.pt
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/detection/yolo$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/detection$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors$ cd ocr
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/ocr$ ls -la
total 20
drwxrwxr-x 5 ubuntu ubuntu 4096 Dec 25 07:14 .
drwxrwxr-x 6 ubuntu ubuntu 4096 Dec 25 07:24 ..
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:14 easyocr
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:14 paddleocr
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:14 tesseract
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/ocr$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors$ cd tracking
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/tracking$ ls -la
total 20
drwxrwxr-x 5 ubuntu ubuntu 4096 Dec 25 07:15 .
drwxrwxr-x 6 ubuntu ubuntu 4096 Dec 25 07:24 ..
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:15 bytetrack
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:15 deepsort
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:15 norfair
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/tracking$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors$ cd pose
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/pose$ ls -la
total 20
drwxrwxr-x 5 ubuntu ubuntu 4096 Dec 25 07:15 .
drwxrwxr-x 6 ubuntu ubuntu 4096 Dec 25 07:24 ..
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:15 mediapipe
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:15 openpose
drwxrwxr-x 2 ubuntu ubuntu 4096 Dec 25 07:15 yolopose
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors/pose$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/sensors$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd vision
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/vision$ ls -la
total 16
drwxr-xr-x 4 ubuntu ubuntu 4096 Feb 14 14:47 .
drwxr-xr-x 7 ubuntu ubuntu 4096 Mar  4 05:13 ..
drwxrwxr-x 4 ubuntu ubuntu 4096 Jan 24 02:32 Kimi-VL-A3B-Thinking-2506
drwxrwxr-x 5 ubuntu ubuntu 4096 Feb 15 06:30 openbmb
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/vision$ cd openbmb
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/vision/openbmb$ ls -la
total 20
drwxrwxr-x 5 ubuntu ubuntu 4096 Feb 15 06:30 .
drwxr-xr-x 4 ubuntu ubuntu 4096 Feb 14 14:47 ..
drwxrwxr-x 3 ubuntu ubuntu 4096 Feb 14 17:18 MiniCPM-SALA
drwxrwxr-x 3 ubuntu ubuntu 4096 Feb 15 06:30 MiniCPM-V-4_5-AWQ
drwxrwxr-x 4 ubuntu ubuntu 4096 Feb 14 14:48 MiniCPM-o-4_5
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/vision/openbmb$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/vision$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd voice
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice$ ls -la
total 16
drwxr-xr-x 4 ubuntu ubuntu 4096 Mar  7 06:32 .
drwxr-xr-x 7 ubuntu ubuntu 4096 Mar  4 05:13 ..
drwxrwxr-x 3 ubuntu ubuntu 4096 Jan 24 02:33 any-any
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  7 06:32 microsoft
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice$ cd any-any
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice/any-any$ ls -la
total 12
drwxrwxr-x 3 ubuntu ubuntu 4096 Jan 24 02:33 .
drwxr-xr-x 4 ubuntu ubuntu 4096 Mar  7 06:32 ..
drwxrwxr-x 4 ubuntu ubuntu 4096 Jan 24 02:33 Chroma-4B
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice/any-any$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice$ cd microsoft
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice/microsoft$ ls -la
total 12
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  7 06:32 .
drwxr-xr-x 4 ubuntu ubuntu 4096 Mar  7 06:32 ..
drwxrwxr-x 7 ubuntu ubuntu 4096 Mar  7 06:32 Phi-4-multimodal-instruct
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice/microsoft$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models/voice$ cd ..
ubuntu@l40s-90-us-west-or-1:/mnt/aetherpro/models$ cd ~/aether-model-node/control/litellm
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/litellm$ ls -la
total 48
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar  9 15:00 .
drwxrwxr-x 4 ubuntu ubuntu 4096 Feb 15 23:59 ..
-rw-r--r-- 1 root   root    517 Mar  9 14:34 .env
drwxrwxr-x 2 ubuntu ubuntu 4096 Mar  5 10:47 aether-data
-rw-r--r-- 1 root   root   4671 Feb 15 10:54 config.bak
-rw-r--r-- 1 root   root   7118 Mar  9 14:56 config.yaml
-rw-r--r-- 1 root   root   1024 Mar  9 15:00 docker-compose.yml
-rw-r--r-- 1 root   root   7050 Feb 16 02:10 legacy.config.yml
-rw-r--r-- 1 root   root    809 Feb 15 07:35 template-compose.yml
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control/litellm$ cd ..
ubuntu@l40s-90-us-west-or-1:~/aether-model-node/control$
