const LABELS = {
  value_proposition: 'Value Proposition',
  business_benefits: 'Business Benefits',
  feasibility: 'Feasibility',
  time_to_market: 'Time to Market',
}

function scoreColor(score) {
  if (score >= 18) return { bar: 'bg-green-500', badge: 'bg-green-100 text-green-800' }
  if (score >= 12) return { bar: 'bg-amber-500', badge: 'bg-amber-100 text-amber-800' }
  return { bar: 'bg-red-500', badge: 'bg-red-100 text-red-800' }
}

export default function ScoreCard({ criterionKey, data }) {
  const { bar, badge } = scoreColor(data.score)
  const pct = (data.score / 25) * 100

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-800 text-sm">{LABELS[criterionKey]}</h3>
        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${badge}`}>
          {data.score}/25
        </span>
      </div>

      <div className="w-full bg-gray-100 rounded-full h-1.5">
        <div
          className={`${bar} h-1.5 rounded-full transition-all duration-500`}
          style={{ width: `${pct}%` }}
        />
      </div>

      <p className="text-sm text-gray-600 leading-relaxed">{data.critique}</p>

      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">
          Suggestions
        </p>
        <ul className="space-y-1.5">
          {data.suggestions.map((s, i) => (
            <li key={i} className="text-sm text-gray-700 flex gap-2">
              <span className="text-blue-500 shrink-0 mt-0.5">→</span>
              {s}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
