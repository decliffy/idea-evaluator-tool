import ScoreCard from './ScoreCard'

const CRITERION_ORDER = ['value_proposition', 'business_benefits', 'feasibility', 'time_to_market']

export default function EvaluationResult({ result, onReset }) {
  const { criteria, total_score, approved, overall_guidance, key_risks, threshold } = result

  return (
    <div className="space-y-6">
      {/* Verdict banner */}
      <div
        className={`rounded-xl p-6 text-center border ${
          approved
            ? 'bg-green-50 border-green-200'
            : 'bg-red-50 border-red-200'
        }`}
      >
        <div
          className={`text-5xl font-black tabular-nums mb-1 ${
            approved ? 'text-green-700' : 'text-red-700'
          }`}
        >
          {total_score}
          <span className="text-2xl font-semibold text-opacity-60">/100</span>
        </div>
        <div
          className={`text-sm font-bold uppercase tracking-widest mt-1 ${
            approved ? 'text-green-600' : 'text-red-600'
          }`}
        >
          {approved ? '✓ Approved' : '✗ Rejected'} — threshold: {threshold}
        </div>
        <p className="mt-2 text-sm text-gray-600 max-w-lg mx-auto">
          {approved
            ? 'This idea clears the bar. Use the per-criterion suggestions below to push it further.'
            : `This idea scored below ${threshold}. Work through the guidance below and resubmit a refined version.`}
        </p>
      </div>

      {/* Score cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {CRITERION_ORDER.map(key => (
          <ScoreCard key={key} criterionKey={key} data={criteria[key]} />
        ))}
      </div>

      {/* Overall guidance */}
      <div className="bg-blue-50 rounded-xl border border-blue-200 p-5">
        <h3 className="font-semibold text-blue-800 mb-3">Overall Guidance</h3>
        <ol className="space-y-2">
          {overall_guidance.map((g, i) => (
            <li key={i} className="text-sm text-blue-900 flex gap-2.5">
              <span className="shrink-0 font-bold text-blue-500">{i + 1}.</span>
              {g}
            </li>
          ))}
        </ol>
      </div>

      {/* Key risks */}
      <div className="bg-amber-50 rounded-xl border border-amber-200 p-5">
        <h3 className="font-semibold text-amber-800 mb-3">Key Risks</h3>
        <ul className="space-y-2">
          {key_risks.map((r, i) => (
            <li key={i} className="text-sm text-amber-900 flex gap-2.5">
              <span className="shrink-0">⚠</span>
              {r}
            </li>
          ))}
        </ul>
      </div>

      {/* Reset */}
      <div className="text-center pb-4">
        <button
          onClick={onReset}
          className="px-6 py-2.5 border border-gray-300 text-sm text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Evaluate Another Idea
        </button>
      </div>
    </div>
  )
}
