import React from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const alerts = [
  {symbol:"AAPL", score:0.94, status:"High", reason:"Volume ratio + VWAP deviation"},
  {symbol:"MSFT", score:0.81, status:"Medium", reason:"Spread z-score"},
  {symbol:"NVDA", score:0.76, status:"Medium", reason:"Return momentum"},
  {symbol:"AMZN", score:0.22, status:"Low", reason:"Normal range"}
];

function App() {
  return <main>
    <header>
      <div><p className="eyebrow">FINSIGHT</p><h1>Financial Intelligence</h1><p className="sub">Anomaly detection, explainability and model feedback</p></div>
      <span className="pill">MODEL v1.0</span>
    </header>

    <section className="cards">
      <div className="card"><span>Alerts today</span><strong>24</strong><small>+12% vs previous day</small></div>
      <div className="card"><span>Confirmed alerts</span><strong>87%</strong><small>Historical feedback accuracy</small></div>
      <div className="card"><span>Model confidence</span><strong>91%</strong><small>Rolling 30-day average</small></div>
      <div className="card"><span>Data quality</span><strong>98.7%</strong><small>Prediction gate: 90%</small></div>
    </section>

    <section className="panel">
      <div className="panel-head"><h2>Detected anomalies</h2><button>Export report</button></div>
      <div className="table">
        <div className="row head"><span>Instrument</span><span>Confidence</span><span>Severity</span><span>Why flagged</span></div>
        {alerts.map(a=><div className="row" key={a.symbol}><span>{a.symbol}</span><span>{Math.round(a.score*100)}%</span><span className={"status "+a.status.toLowerCase()}>{a.status}</span><span>{a.reason}</span></div>)}
      </div>
    </section>

    <section className="grid">
      <div className="panel"><h2>Feature contribution</h2><div className="bars">{[
        ["Volume ratio vs 20-day avg",82],["Rolling VWAP deviation",67],["Spread z-score",48],["Intraday momentum",31]
      ].map(([name,v])=><div className="bar" key={String(name)}><label>{name}<b>{v}%</b></label><i><em style={{width:`${v}%`}}/></i></div>)}</div></div>
      <div className="panel"><h2>Feedback loop</h2><p className="big">312</p><p className="muted">alerts labelled by analysts</p><p>Confirmed <b>274</b></p><p>False positive <b>38</b></p></div>
    </section>
  </main>
}
createRoot(document.getElementById("root")!).render(<App />);
