export function Card({ title, children, sub }) { return <section className="card"><div className="card-head"><div><b>{title}</b>{sub && <small>{sub}</small>}</div></div>{children}</section>; }
export function Badge({ children, tone = 'neutral' }) { return <span className={`badge ${tone}`}>{children}</span>; }
