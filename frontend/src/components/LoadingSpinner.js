import "./LoadingSpinner.css"

function LoadingSpinner() {
  return (
    <div className="loading-overlay">
      <div className="spinner">
        <div className="spinner-ring"></div>
        <p>Parsing your statement...</p>
      </div>
    </div>
  )
}

export default LoadingSpinner
