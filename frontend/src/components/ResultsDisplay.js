import "./ResultsDisplay.css"

function ResultsDisplay({ results }) {
  const dataPoints = results.data_points || {}

  const dataPointLabels = {
    card_last_4: "Card Last 4 Digits",
    billing_cycle: "Billing Cycle",
    payment_due_date: "Payment Due Date",
    total_balance: "Total Balance",
    card_variant: "Card Variant",
  }

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Parsed Results</h2>
        <p className="issuer-badge">{results.issuer}</p>
      </div>

      <div className="data-points-grid">
        {Object.entries(dataPointLabels).map(([key, label]) => (
          <div key={key} className="data-point-card">
            <h3 className="data-point-label">{label}</h3>
            <p className="data-point-value">{dataPoints[key] || "Not found"}</p>
          </div>
        ))}
      </div>

      <div className="results-info">
        <p>All data has been extracted from your statement. No data is stored on our servers.</p>
      </div>
    </div>
  )
}

export default ResultsDisplay
