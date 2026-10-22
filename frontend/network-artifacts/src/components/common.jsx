export function Card({ title, children, action }) { return <section className="card">{title && <div className="card-head"><h3>{title}</h3>{action}</div>}{children}</section>; }
export function Badge({ children, tone = 'neutral' }) { return <span className={`badge ${tone}`}>{children}</span>; }
export function Metric({ label, value, sub }) { return <div className="metric"><span>{label}</span><strong>{value}</strong>{sub && <small>{sub}</small>}</div>; }
export function Empty({ children }) { return <div className="empty">{children}</div>; }
