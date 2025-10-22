const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000"

class APIService {
  async getIssuers() {
    try {
      const response = await fetch(`${API_URL}/api/issuers`)
      if (!response.ok) {
        throw new Error("Failed to fetch issuers")
      }
      return await response.json()
    } catch (error) {
      console.error("Error fetching issuers:", error)
      throw error
    }
  }

  async parseStatement(file, issuer) {
    try {
      const formData = new FormData()
      formData.append("file", file)
      formData.append("issuer", issuer)

      const response = await fetch(`${API_URL}/api/parse`, {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Failed to parse statement")
      }

      return data
    } catch (error) {
      console.error("Error parsing statement:", error)
      throw error
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${API_URL}/api/health`)
      return response.ok
    } catch (error) {
      console.error("Health check failed:", error)
      return false
    }
  }
}

export default new APIService()
