import { useState } from 'react'
import IdeaForm from './components/IdeaForm'
import EvaluationResult from './components/EvaluationResult'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(idea) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      // CloudFront's OAC signs requests to the Lambda function URL and Lambda
      // rejects unsigned payloads, so the client must send the SHA-256 of the
      // exact request body in x-amz-content-sha256. (crypto.subtle requires a
      // secure context, which CloudFront/HTTPS and localhost both satisfy.)
      const body = JSON.stringify({ idea })
      const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(body))
      const bodyHash = Array.from(new Uint8Array(digest))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('')
      const res = await fetch('/api/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-amz-content-sha256': bodyHash,
        },
        body,
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || 'Evaluation failed')
      }
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-5">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900">Idea Evaluator</h1>
          <p className="text-sm text-gray-500 mt-1">
            Submit your business idea for a structured critique and score across four dimensions.
          </p>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-6 py-8">
        {result ? (
          <EvaluationResult result={result} onReset={() => setResult(null)} />
        ) : (
          <IdeaForm onSubmit={handleSubmit} loading={loading} error={error} />
        )}
      </main>
    </div>
  )
}
