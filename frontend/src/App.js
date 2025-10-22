
"use client"

import { useState, useEffect } from "react"
import "./App.css"
import IssuerSelector from "./components/IssuerSelector"
import FileUploader from "./components/FileUploader"
import ResultsDisplay from "./components/ResultsDisplay"
import LoadingSpinner from "./components/LoadingSpinner"
import ErrorBoundary from "./components/ErrorBoundary"
import APIService from "./services/api"

function App() {
  const [selectedIssuer, setSelectedIssuer] = useState(null)
  const [issuers, setIssuers] = useState([])
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [apiAvailable, setApiAvailable] = useState(true)

  useEffect(() => {
    fetchIssuers()
    checkAPIHealth()
  }, [])

  const checkAPIHealth = async () => {
    const isHealthy = await APIService.healthCheck()
    setApiAvailable(isHealthy)
    if (!isHealthy) {
      setError("Backend API is not available. Please ensure Flask server is running on port 5000.")
    }
  }

  const fetchIssuers = async () => {
    try {
      const data = await APIService.getIssuers()
      setIssuers(data)
    } catch (err) {
      setError("Failed to load card issuers. Please check your connection.")
      console.error(err)
    }
  }

  const handleIssuerSelect = (issuer) => {
    setSelectedIssuer(issuer)
    setResults(null)
    setError(null)
  }

  const handleFileUpload = async (file) => {
    if (!selectedIssuer) {
      setError("Please select a card issuer first")
      return
    }

    if (!apiAvailable) {
      setError("Backend API is not available. Please ensure Flask server is running.")
      return
    }

    setLoading(true)
    setError(null)

    try {
      const data = await APIService.parseStatement(file, selectedIssuer.id)
      setResults(data)
    } catch (err) {
      setError(err.message)
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedIssuer(null)
    setResults(null)
    setError(null)
  }

  return (
    <ErrorBoundary>
      <div className="app">
        <header className="app-header">
          <h1>Credit Card Statement Parser</h1>
          <p>Extract key data from your credit card statements</p>
        </header>

        <main className="app-main">
          {!results ? (
            <div className="upload-section">
              {!apiAvailable && (
                <div className="warning-message">
                  <strong>Warning:</strong> Backend API is not available. Make sure Flask server is running on port
                  5000.
                </div>
              )}

              <IssuerSelector issuers={issuers} selectedIssuer={selectedIssuer} onSelect={handleIssuerSelect} />

              {selectedIssuer && (
                <FileUploader onFileUpload={handleFileUpload} loading={loading} issuer={selectedIssuer} />
              )}

              {error && <div className="error-message">{error}</div>}
            </div>
          ) : (
            <div className="results-section">
              <ResultsDisplay results={results} />
              <button className="reset-button" onClick={handleReset}>
                Parse Another Statement
              </button>
            </div>
          )}

          {loading && <LoadingSpinner />}
        </main>

        <footer className="app-footer">
          <p>Secure PDF parsing - Your data is not stored on our servers</p>
        </footer>
      </div>
    </ErrorBoundary>
  )
}

export default App;
