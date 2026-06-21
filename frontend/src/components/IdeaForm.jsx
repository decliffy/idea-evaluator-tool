import { useState } from 'react'

const MIN_LENGTH = 30

export default function IdeaForm({ onSubmit, loading, error }) {
  const [idea, setIdea] = useState('')
  const tooShort = idea.trim().length > 0 && idea.trim().length < MIN_LENGTH

  function handleSubmit(e) {
    e.preventDefault()
    if (idea.trim().length >= MIN_LENGTH) onSubmit(idea.trim())
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-800 mb-1">Describe your idea</h2>
      <p className="text-sm text-gray-500 mb-4">
        Include the problem you're solving, your target audience, and your proposed solution. More detail leads to better analysis.
      </p>
      <form onSubmit={handleSubmit}>
        <textarea
          value={idea}
          onChange={e => setIdea(e.target.value)}
          disabled={loading}
          rows={9}
          placeholder="e.g. An AI-powered tool that helps small business owners automatically draft and send personalized follow-up emails after sales calls, pulling context from CRM notes to save 2–3 hours per week..."
          className="w-full border border-gray-300 rounded-lg p-3 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none disabled:bg-gray-50 placeholder:text-gray-400"
        />
        <div className="mt-2 flex items-center justify-between">
          <span className={`text-xs ${tooShort ? 'text-amber-600' : 'text-gray-400'}`}>
            {tooShort
              ? `${MIN_LENGTH - idea.trim().length} more characters needed`
              : `${idea.length} characters`}
          </span>
        </div>
        {error && (
          <p className="mt-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            {error}
          </p>
        )}
        <div className="mt-4 flex justify-end">
          <button
            type="submit"
            disabled={loading || idea.trim().length < MIN_LENGTH}
            className="px-6 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Evaluating…
              </span>
            ) : (
              'Evaluate Idea'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
