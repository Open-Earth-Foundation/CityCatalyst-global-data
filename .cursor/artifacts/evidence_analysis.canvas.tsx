import React, { useState } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';

export default function EvidenceAnalysis() {
  const [activeTab, setActiveTab] = useState('overview');

  // Document Usage Data
  const documentUsage = [
    { name: 'PARC Los Ríos', items: 762, actions: 101, percentage: 100 }
  ];

  // Signal Types Distribution
  const signalTypeData = [
    { name: 'Action', value: 428, pct: 56.2 },
    { name: 'Context', value: 162, pct: 21.3 },
    { name: 'Target', value: 62, pct: 8.1 },
    { name: 'Risk', value: 60, pct: 7.9 },
    { name: 'Funding', value: 38, pct: 5.0 },
    { name: 'Governance', value: 12, pct: 1.6 }
  ];

  // Signal Strength Distribution
  const strengthData = [
    { name: 'High', value: 72, pct: 9.4, color: '#10b981' },
    { name: 'Medium', value: 658, pct: 86.4, color: '#f59e0b' },
    { name: 'Low', value: 32, pct: 4.2, color: '#ef4444' }
  ];

  // Signal Relation Distribution
  const relationData = [
    { name: 'Commits', value: 289, pct: 37.9 },
    { name: 'Contextualizes', value: 178, pct: 23.4 },
    { name: 'Prioritizes', value: 132, pct: 17.3 },
    { name: 'Identifies', value: 65, pct: 8.5 },
    { name: 'Targets', value: 50, pct: 6.6 },
    { name: 'Funds', value: 30, pct: 3.9 },
    { name: 'Governs', value: 16, pct: 2.1 },
    { name: 'Monitors', value: 2, pct: 0.3 }
  ];

  // Score Distribution
  const scoreData = [
    { name: 'Strong (≥0.7)', value: 0, color: '#059669' },
    { name: 'Moderate (0.4-0.7)', value: 98, color: '#f59e0b' },
    { name: 'Weak (<0.4)', value: 3, color: '#dc2626' }
  ];

  // Quality Metrics
  const qualityData = [
    { name: 'Explicit', value: 483, pct: 63.4, color: '#3b82f6' },
    { name: 'Inferred', value: 279, pct: 36.6, color: '#9ca3af' }
  ];

  const relevanceData = [
    { name: 'High', value: 30, pct: 3.9, color: '#10b981' },
    { name: 'Medium', value: 519, pct: 68.1, color: '#f59e0b' },
    { name: 'Low', value: 213, pct: 28.0, color: '#ef4444' }
  ];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  const topActions = [
    { id: 1, name: 'Develop integrated renewable energy planning', score: 0.5, evidence: 20, category: 'moderate' },
    { id: 2, name: 'Retrofit commercial institutional buildings', score: 0.5, evidence: 17, category: 'moderate' },
    { id: 3, name: 'Energy-efficient climate-resilient housing', score: 0.562, evidence: 16, category: 'moderate' },
    { id: 4, name: 'Accelerate Agroforestry adoption', score: 0.588, evidence: 16, category: 'moderate' },
    { id: 5, name: 'Retrofit residential buildings efficiency', score: 0.527, evidence: 15, category: 'moderate' },
    { id: 6, name: 'Ecological and agroclimatic mapping', score: 0.540, evidence: 15, category: 'moderate' },
    { id: 7, name: 'Improve public transport modal shift', score: 0.393, evidence: 15, category: 'weak' },
    { id: 8, name: 'Optimize energy efficiency standards', score: 0.5, evidence: 14, category: 'moderate' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Evidence Analysis Report</h1>
          <p className="text-lg text-slate-600">CL ZAL (Valdivia) - Los Ríos Region (14)</p>
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-900">
              <strong>Dataset:</strong> All 762 evidence items from Plan de Acción Regional de Cambio Climático (PARC) Los Ríos
            </p>
            <p className="text-sm text-blue-900 mt-2">
              <strong>Coverage:</strong> 101 climate actions mapped to regional policy documents (no municipal-level docs available)
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 flex-wrap">
          {[
            { key: 'overview', label: '📊 Overview' },
            { key: 'quality', label: '⚠️ Quality Assessment' },
            { key: 'signals', label: '📡 Signal Analysis' },
            { key: 'coverage', label: '🎯 Coverage & Gaps' }
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === tab.key
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* OVERVIEW TAB */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Total Evidence Items</p>
                <p className="text-3xl font-bold text-blue-600">762</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Climate Actions</p>
                <p className="text-3xl font-bold text-green-600">101</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Source Documents</p>
                <p className="text-3xl font-bold text-orange-600">1</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Avg Evidence/Action</p>
                <p className="text-3xl font-bold text-purple-600">7.5</p>
              </div>
            </div>

            {/* Document Usage */}
            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">📋 Document Coverage</h2>
              <div className="space-y-4">
                <div className="p-4 bg-slate-50 rounded border border-slate-200">
                  <p className="font-semibold text-slate-900">Plan de Acción Regional de Cambio Climático Los Ríos</p>
                  <p className="text-sm text-slate-600 mt-2">
                    ✓ 762 evidence items (100% of all evidence)
                  </p>
                  <p className="text-sm text-slate-600">
                    ✓ Supports 101 unique climate actions
                  </p>
                  <p className="text-sm text-slate-600 mt-2">
                    <strong>Assessment:</strong> <span className="text-orange-600">⚠️ Single source of evidence</span> - All evidence comes from one regional document. No municipal-level plans (PACCC) available for Valdivia.
                  </p>
                </div>
              </div>
            </div>

            {/* Signal Type Distribution */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Signal Type Distribution</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie data={signalTypeData} cx="50%" cy="50%" labelLine={false} label={({ name, pct }) => `${name} (${pct}%)`} outerRadius={80} fill="#8884d8" dataKey="value">
                      {signalTypeData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value} items`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Signal Strength Breakdown</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={strengthData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" radius={8}>
                      {strengthData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
                <div className="mt-4 text-sm text-slate-600">
                  <p>🟢 <strong>High (9.4%):</strong> Only 72 items with high signal strength - limited strong support</p>
                  <p className="mt-2">🟡 <strong>Medium (86.4%):</strong> Majority of evidence has medium strength - moderate policy support</p>
                  <p className="mt-2">🔴 <strong>Low (4.2%):</strong> Few weak signals</p>
                </div>
              </div>
            </div>

            {/* Score Distribution */}
            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">Policy Support Score Distribution</h2>
              <div className="grid md:grid-cols-3 gap-4">
                {scoreData.map(item => (
                  <div key={item.name} className="p-4 rounded-lg border-2" style={{ borderColor: item.color, backgroundColor: item.color + '10' }}>
                    <p className="text-lg font-bold" style={{ color: item.color }}>{item.value}</p>
                    <p className="text-sm text-slate-600">{item.name}</p>
                  </div>
                ))}
              </div>
              <p className="text-sm text-slate-600 mt-4">
                ⚠️ <strong>No "Strong" support:</strong> No actions achieved high (≥0.7) policy support scores. 98 actions have "moderate" support (0.4-0.7), indicating consistent but not overwhelming policy backing.
              </p>
            </div>
          </div>
        )}

        {/* QUALITY TAB */}
        {activeTab === 'quality' && (
          <div className="space-y-8">
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
              <h3 className="font-bold text-yellow-900">⚠️ Evidence Quality Alert</h3>
              <p className="text-sm text-yellow-800 mt-2">
                64.7% of evidence is derived or inferred rather than directly stated. This affects confidence in conclusions.
              </p>
            </div>

            {/* Explicitness */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Explicitness of Evidence</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie data={qualityData} cx="50%" cy="50%" labelLine={false} label={({ name, pct }) => `${name}\n${pct}%`} outerRadius={80} fill="#8884d8" dataKey="value">
                      {qualityData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value} items`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Document Relevance</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={relevanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" radius={8}>
                      {relevanceData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Quality Issues */}
            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">Quality Assessment</h2>
              <div className="space-y-4">
                <div className="p-4 bg-red-50 border-l-4 border-red-300 rounded">
                  <p className="font-semibold text-red-900">❌ Inferred Evidence (36.6%)</p>
                  <p className="text-sm text-red-800 mt-1">
                    279 items are inferred rather than explicitly stated in documents. This weakens direct policy support claims.
                  </p>
                  <p className="text-xs text-red-700 mt-2">
                    <strong>Concern:</strong> Conclusions about policy commitment may be overstated when based on inference.
                  </p>
                </div>

                <div className="p-4 bg-yellow-50 border-l-4 border-yellow-300 rounded">
                  <p className="font-semibold text-yellow-900">⚠️ Medium/Low Relevance (96.1%)</p>
                  <p className="text-sm text-yellow-800 mt-1">
                    732 items rated as "medium" or "low" relevance. Only 30 items have "high" relevance to specific actions.
                  </p>
                  <p className="text-xs text-yellow-700 mt-2">
                    <strong>Concern:</strong> Evidence often requires interpretation to connect to the specific climate action.
                  </p>
                </div>

                <div className="p-4 bg-blue-50 border-l-4 border-blue-300 rounded">
                  <p className="font-semibold text-blue-900">ℹ️ Single Document Source (100%)</p>
                  <p className="text-sm text-blue-800 mt-1">
                    All 762 items come from one regional PARC document. No corroboration from other sources (sectoral plans, municipal PACCC, etc.).
                  </p>
                  <p className="text-xs text-blue-700 mt-2">
                    <strong>Concern:</strong> Cannot triangulate findings or validate consistency with other policy instruments.
                  </p>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-green-50 border border-green-200 p-6 rounded-lg">
              <h2 className="text-xl font-bold text-green-900 mb-4">✅ Recommendations to Strengthen Evidence</h2>
              <ul className="space-y-2 text-sm text-green-900">
                <li>• <strong>Add municipal-level documents:</strong> Source PACCC (Plan de Acción Comunal de Cambio Climático) for Valdivia to validate regional-level evidence</li>
                <li>• <strong>Include sectoral plans:</strong> Transport, energy, waste management sector plans to corroborate actions</li>
                <li>• <strong>Validate inferred evidence:</strong> Cross-reference 279 inferred items with document authors or regional authorities</li>
                <li>• <strong>Prioritize explicit evidence:</strong> Focus first on the 483 (63.4%) explicitly-stated evidence items</li>
                <li>• <strong>Re-score with multiple sources:</strong> When more documents are available, recalculate policy support scores</li>
              </ul>
            </div>
          </div>
        )}

        {/* SIGNALS TAB */}
        {activeTab === 'signals' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Signal Relations</h2>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={relationData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="name" width={100} tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#3b82f6" radius={8} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Signal Relation Interpretation</h2>
                <div className="space-y-3 text-sm">
                  <div>
                    <p className="font-semibold text-slate-900">📌 Commits (37.9%)</p>
                    <p className="text-slate-600">Regional government explicitly commits to action - strongest support</p>
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">🔄 Contextualizes (23.4%)</p>
                    <p className="text-slate-600">Provides background/context for action - indirect support</p>
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">⭐ Prioritizes (17.3%)</p>
                    <p className="text-slate-600">Action identified as priority - medium support</p>
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">🎯 Targets (6.6%)</p>
                    <p className="text-slate-600">Specific targets/metrics set - concrete support</p>
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">💰 Funds (3.9%)</p>
                    <p className="text-slate-600">Funding allocated - strongest concrete commitment</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">Key Finding</h2>
              <p className="text-slate-700 mb-3">
                Most evidence (37.9%) shows the region "<strong>commits</strong>" to actions. However, fewer items show regional government:
              </p>
              <ul className="space-y-2 text-sm text-slate-600 ml-4">
                <li>✓ Setting concrete targets (6.6%)</li>
                <li>✓ Allocating funding (3.9%)</li>
                <li>✓ Establishing governance mechanisms (2.1%)</li>
              </ul>
              <p className="text-sm text-orange-600 font-semibold mt-4">
                ⚠️ Gap: Regional PARC expresses commitment but lacks concrete targets, timelines, or funding allocations for most actions.
              </p>
            </div>
          </div>
        )}

        {/* COVERAGE TAB */}
        {activeTab === 'coverage' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Top 8 Most-Supported Actions</h2>
                <div className="space-y-3">
                  {topActions.map((action, idx) => (
                    <div key={action.id} className="p-3 bg-slate-50 rounded border border-slate-200">
                      <p className="font-semibold text-sm text-slate-900">{idx + 1}. {action.name.substring(0, 50)}...</p>
                      <div className="flex justify-between items-center mt-2">
                        <span className={`text-xs font-semibold px-2 py-1 rounded ${
                          action.category === 'strong' ? 'bg-green-100 text-green-800' :
                          action.category === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {action.category.toUpperCase()} ({action.score.toFixed(3)})
                        </span>
                        <span className="text-xs text-slate-600">{action.evidence} items</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h2 className="text-xl font-bold text-slate-900 mb-4">Coverage Assessment</h2>
                <div className="space-y-4">
                  <div className="p-4 bg-green-50 border-l-4 border-green-300 rounded">
                    <p className="font-semibold text-green-900">✅ Broad Coverage</p>
                    <p className="text-sm text-green-800">101 climate actions mapped to evidence - demonstrates comprehensive policy analysis across sectors</p>
                  </div>

                  <div className="p-4 bg-orange-50 border-l-4 border-orange-300 rounded">
                    <p className="font-semibold text-orange-900">⚠️ Shallow Depth per Action</p>
                    <p className="text-sm text-orange-800">Average 7.5 evidence items per action is relatively low. Top actions only have 15-20 items. Most actions share same PARC source.</p>
                  </div>

                  <div className="p-4 bg-red-50 border-l-4 border-red-300 rounded">
                    <p className="font-semibold text-red-900">❌ No Municipal Validation</p>
                    <p className="text-sm text-red-800">Evidence comes only from regional PARC. Without city-level PACCC, cannot confirm if regional commitments translate to local action in Valdivia.</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">🎯 Critical Gaps</h2>
              <div className="space-y-3 text-sm">
                <div className="flex gap-3">
                  <span className="text-lg">1️⃣</span>
                  <div>
                    <p className="font-semibold text-slate-900">No municipal-level documents</p>
                    <p className="text-slate-600">Valdivia may have its own PACCC or sectoral plans not included in analysis</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <span className="text-lg">2️⃣</span>
                  <div>
                    <p className="font-semibold text-slate-900">No sectoral plans included</p>
                    <p className="text-slate-600">Transport, energy, waste, agriculture sectoral plans would provide specific targets/timelines</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <span className="text-lg">3️⃣</span>
                  <div>
                    <p className="font-semibold text-slate-900">No budget/finance documents</p>
                    <p className="text-slate-600">Regional budget allocations for climate actions not analyzed</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <span className="text-lg">4️⃣</span>
                  <div>
                    <p className="font-semibold text-slate-900">No implementation timelines</p>
                    <p className="text-slate-600">Regional PARC discusses commitments but lacks phasing/timelines for most actions</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
              <h2 className="text-xl font-bold text-blue-900 mb-4">💡 Conclusion</h2>
              <p className="text-blue-900 text-sm leading-relaxed">
                The analysis provides a <strong>broad but shallow</strong> view of regional policy support for 101 climate actions. 
                All evidence comes from a single PARC document with 64% inferred/indirect connections. While the regional government 
                clearly commits to action, the evidence lacks <strong>specificity, municipal validation, and concrete targets</strong>. 
                To strengthen conclusions, incorporate municipal-level documents, sectoral plans, and budget data before making 
                investment or implementation decisions.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
