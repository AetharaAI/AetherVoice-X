import type { PropsWithChildren, ReactNode } from "react";

export function Panel({ title, eyebrow, children }: PropsWithChildren<{ title: string; eyebrow?: ReactNode }>) {
  return (
    <section className="panel">
      <header className="panel-header">
        <div>
          {eyebrow ? <div className="eyebrow">{eyebrow}</div> : null}
          <h2>{title}</h2>
        </div>
      </header>
      {children}
    </section>
  );
}
