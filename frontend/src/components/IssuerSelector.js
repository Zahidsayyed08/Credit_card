"use client"
import "./IssuerSelector.css"

function IssuerSelector({ issuers, selectedIssuer, onSelect }) {
  return (
    <div className="issuer-selector">
      <h2>Step 1: Select Your Card Issuer</h2>
      <div className="issuer-grid">
        {issuers.map((issuer) => (
          <button
            key={issuer.id}
            className={`issuer-card ${selectedIssuer?.id === issuer.id ? "active" : ""}`}
            onClick={() => onSelect(issuer)}
          >
            <span className="issuer-logo">{issuer.logo}</span>
            <span className="issuer-name">{issuer.name}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default IssuerSelector
