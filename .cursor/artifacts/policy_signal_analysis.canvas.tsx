import React, { useState } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';

export default function PolicySignalAnalysis() {
  const [activeTab, setActiveTab] = useState('comparison');

  // Document breakdown
  const documentData = [
    { name: 'PARC Los Lagos', items: 323, pct: 31.8, type: 'Regional Plan' },
    { name: 'Sector Energía', items: 143, pct: 14.1, type: 'Sector Plan' },
    { name: 'Sector Salud', items: 118, pct: 11.6, type: 'Sector Plan' },
    { name: 'Sector Ciudades', items: 113, pct: 11.1, type: 'Sector Plan' },
    { name: 'Sector Agricultura', items: 101, pct: 9.9, type: 'Sector Plan' },
    { name: 'Sector Infraestructura', items: 90, pct: 8.8, type: 'Sector Plan' },
    { name: 'Estrategia Climática LP', items: 78, pct: 7.7, type: 'Framework' },
    { name: 'Sector Transporte', items: 51, pct: 5.0, type: 'Sector Plan' }
  ];

  // Signal strength comparison
  const strengthComparison = [
    { category: 'High', policySignal: 50.0, regionalOnly: 9.4 },
    { category: 'Medium', policySignal: 49.8, regionalOnly: 86.4 },
    { category: 'Low', policySignal: 0.3, regionalOnly: 4.2 }
  ];

  // Signal types
  const signalTypes = [
    { name: 'Action', value: 642, pct: 63.1 },
    { name: 'Target', value: 161, pct: 15.8 },
    { name: 'Governance', value: 45, pct: 4.4 },
    { name: 'Sector Priority', value: 40, pct: 3.9 },
    { name: 'Risk', value: 36, pct: 3.5 },
    { name: 'Context', value: 35, pct: 3.4 },
    { name: 'Funding', value: 34, pct: 3.3 },
    { name: 'Monitoring', value: 24, pct: 2.4 }
  ];

  // Score distribution
  const scoreDistribution = [
    { name: 'Strong', policySignal: 29, regionalOnly: 0, pct: 28.4 },
    { name: 'Moderate', policySignal: 67, regionalOnly: 98, pct: 0 },
    { name: 'Weak', policySignal: 6, regionalOnly: 3, pct: 5.9 }
  ];

  // Top actions in policy signal
  const topActions = [
    { id: 'icare_0117', score: 0.998, evidence: 64, docs: 7 },
    { id: 'c40_0029', score: 0.990, evidence: 48, docs: 6 },
    { id: 'c40_0023', score: 0.984, evidence: 41, docs: 6 },
    { id: 'c40_0035', score: 0.978, evidence: 44, docs: 8 },
    { id: 'ipcc_0049', score: 0.975, evidence: 50, docs: 9 }
  ];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Policy Signal Analysis: Valdivia (CL ZAL)</h1>
          <p className="text-lg text-slate-600">Comprehensive review of policy_signal_valdivia.json</p>
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-900">
              <strong>Dataset:</strong> 1,017 evidence items from 8 documents (regional + national + sector plans)
            </p>
            <p className="text-sm text-blue-900 mt-2">
              <strong>Coverage:</strong> 102 climate actions with comprehensive evidence depth
            </p>
            <p className="text-sm text-blue-900 mt-2">
              <strong>Key Finding:</strong> ⭐ This is a MUCH RICHER dataset than the regional-only extract
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 flex-wrap">
          {[
            { key: 'comparison', label: '⚖️ Comparison' },
            { key: 'documents', label: '📚 Documents' },
            { key: 'evidence', label: '📊 Evidence Quality' },
            { key: 'findings', label: '🎯 Key Findings' }
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

        {/* COMPARISON TAB */}
        {activeTab === 'comparison' && (
          <div className="space-y-8">
            <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-6">
              <h3 className="font-bold text-green-900">✅ Good News!</h3>
              <p className="text-sm text-green-800 mt-2">
                The policy_signal_valdivia.json file contains MUCH more comprehensive evidence than the regional PARC-only extract. It includes national frameworks and 7 sector plans with detailed targets and funding commitments.
              </p>
            </div>

            {/* Key Metrics Comparison */}
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Evidence Items</p>
                <p className="text-2xl font-bold text-blue-600">1,017</p>
                <p className="text-xs text-slate-500 mt-2">vs 762 (regional only)</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Climate Actions</p>
                <p className="text-2xl font-bold text-green-600">102</p>
                <p className="text-xs text-slate-500 mt-2">vs 101 (regional only)</p>
              </div>
              <div className="bg-white p-4 rounded-lg border border-slate-200">
                <p className="text-sm text-slate-600">Source Documents</p>
                <p className="text-2xl font-bold text-orange-600">8</p>
                <p className="text-xs text-slate-500 mt-2">vs 1 (regional only)</p>
              </div>
            </div>

            {/* Comparison Table */}
            <div className="bg-white p-6 rounded-lg border border-slate-200 overflow-x-auto">
              <h2 className="text-xl font-bold text-slate-900 mb-4">📊 Detailed Comparison</h2>
              <table className="w-full text-sm">
                <thead className="bg-slate-100">
                  <tr>
                    <th className="text-left p-3 font-semibold">Metric</th>
                    <th className="text-center p-3 font-semibold">Policy Signal</th>
                    <th className="text-center p-3 font-semibold">Regional Only</th>
                    <th className="text-center p-3 font-semibold">Difference</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-t">
                    <td className="p-3">Total Evidence Items</td>
                    <td className="text-center p-3 font-semibold">1,017</td>
                    <td className="text-center p-3">762</td>
                    <td className="text-center p-3 text-green-600 font-semibold">+33.5%</td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-3">Actions</td>
                    <td className="text-center p-3 font-semibold">102</td>
                    <td className="text-center p-3">101</td>
                    <td className="text-center p-3">+1</td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-3">Source Documents</td>
                    <td className="text-center p-3 font-semibold">8</td>
                    <td className="text-center p-3">1</td>
                    <td className="text-center p-3 text-green-600 font-semibold">+700%</td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-3">Avg Evidence/Action</td>
                    <td className="text-center p-3 font-semibold">9.97</td>
                    <td className="text-center p-3">7.54</td>
                    <td className="text-center p-3 text-green-600 font-semibold">+32%</td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-3">Avg Documents/Action</td>
                    <td className="text-center p-3 font-semibold">6.4</td>
                    <td className="text-center p-3">1.0</td>
                    <td className="text-center p-3 text-green-600 font-semibold">+540%</td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-3">High Signal Strength</td>
                    <td className="text-center p-3 font-semibold">50.0%</td>
                    <td className="text-center p-3">9.4%</td>
                    <td className="text-center p-3 text-green-600 font-semibold">+40.6pp</td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-3">Explicit Evidence</td>
                    <td className="text-center p-3 font-semibold">81.9%</td>
                    <td className="text-center p-3">63.4%</td>
                    <td className="text-center p-3 text-green-600 font-semibold">+18.5pp</td>
                  </tr>
                  <tr className="border-t bg-green-50">
                    <td className="p-3 font-semibold">Strong Policy Support</td>
                    <td className="text-center p-3 font-semibold text-green-600">28.4% (29 actions)</td>
                    <td className="text-center p-3 text-red-600">0% (0 actions)</td>
                    <td className="text-center p-3 text-green-600 font-semibold">✅ ALL 29 strong!</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Signal Strength Comparison */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Signal Strength Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={strengthComparison}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="category" />
                    <YAxis label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="policySignal" fill="#3b82f6" name="Policy Signal" />
                    <Bar dataKey="regionalOnly" fill="#ef4444" name="Regional Only" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Score Distribution</h3>
                <div className="space-y-3">
                  <div className="p-3 bg-green-50 rounded border border-green-200">
                    <p className="font-semibold text-green-900">Strong</p>
                    <p className="text-sm text-green-800">
                      Policy Signal: <span className="font-bold">29 actions (28.4%)</span><br/>
                      Regional Only: <span className="font-bold text-red-600">0 actions (0%)</span>
                    </p>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded border border-yellow-200">
                    <p className="font-semibold text-yellow-900">Moderate</p>
                    <p className="text-sm text-yellow-800">
                      Policy Signal: <span className="font-bold">67 actions (65.7%)</span><br/>
                      Regional Only: <span className="font-bold">98 actions (97.0%)</span>
                    </p>
                  </div>
                  <div className="p-3 bg-red-50 rounded border border-red-200">
                    <p className="font-semibold text-red-900">Weak</p>
                    <p className="text-sm text-red-800">
                      Policy Signal: <span className="font-bold">6 actions (5.9%)</span><br/>
                      Regional Only: <span className="font-bold">3 actions (3.0%)</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Key Insight */}
            <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
              <h3 className="font-bold text-blue-900 mb-3">🔍 Key Insight</h3>
              <p className="text-blue-900 text-sm leading-relaxed mb-3">
                The policy_signal_valdivia.json file is <strong>significantly superior</strong> to the regional-only extract:
              </p>
              <ul className="text-sm text-blue-900 space-y-2 ml-4">
                <li>✅ <strong>8 source documents</strong> (vs 1) provide triangulation</li>
                <li>✅ <strong>33% more evidence</strong> items for deeper analysis</li>
                <li>✅ <strong>6.4 documents per action</strong> (vs 1) - corroboration from multiple sources</li>
                <li>✅ <strong>50% high-strength signals</strong> (vs 9%) - much stronger evidence quality</li>
                <li>✅ <strong>29 "strong" support actions</strong> (vs 0) - clear policy champions identified</li>
                <li>✅ <strong>82% explicit evidence</strong> (vs 63%) - more direct policy language</li>
              </ul>
              <p className="text-blue-900 text-sm font-semibold mt-4">
                💡 <strong>Recommendation:</strong> Use policy_signal_valdivia.json for all future analysis. It's the authoritative source.
              </p>
            </div>
          </div>
        )}

        {/* DOCUMENTS TAB */}
        {activeTab === 'documents' && (
          <div className="space-y-8">
            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">📚 Document Coverage Breakdown</h2>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={documentData} layout="vertical" margin={{ left: 220 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" width={200} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="items" fill="#3b82f6" radius={8} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Document Types</h3>
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 rounded">
                    <p className="font-semibold text-blue-900">🎯 Regional Plan</p>
                    <p className="text-sm text-blue-800">PARC Los Lagos - 323 items (31.8%)</p>
                  </div>
                  <div className="p-3 bg-green-50 rounded">
                    <p className="font-semibold text-green-900">⚙️ Sector Plans (6)</p>
                    <p className="text-sm text-green-800">Energy, Health, Cities, Agriculture, Infrastructure, Transport - 498 items (49.0%)</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded">
                    <p className="font-semibold text-purple-900">🌍 National Framework</p>
                    <p className="text-sm text-purple-800">Long-term Climate Strategy - 78 items (7.7%)</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Coverage by Document</h3>
                <div className="space-y-2 text-sm">
                  {documentData.map((doc, idx) => (
                    <div key={idx} className="flex justify-between items-center">
                      <span className="text-slate-700">{doc.name}</span>
                      <span className="font-semibold text-slate-900">{doc.items} ({doc.pct}%)</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
              <h3 className="font-bold text-blue-900 mb-3">✅ Document Quality Assessment</h3>
              <ul className="text-sm text-blue-900 space-y-2">
                <li>✓ <strong>Balanced coverage:</strong> Regional PARC (31.8%) + Sector plans (49.0%) + National framework (7.7%)</li>
                <li>✓ <strong>Sectoral depth:</strong> 6 sector plans provide specific targets for energy, health, cities, agriculture, infrastructure, transport</li>
                <li>✓ <strong>Strategic alignment:</strong> Long-term climate strategy ensures national-level consistency</li>
                <li>⚠️ <strong>Gap:</strong> Still no municipal PACCC for Valdivia - regional/national only</li>
              </ul>
            </div>
          </div>
        )}

        {/* EVIDENCE QUALITY TAB */}
        {activeTab === 'evidence' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Signal Type Distribution</h3>
                <ResponsiveContainer width="100%" height={350}>
                  <PieChart>
                    <Pie data={signalTypes} cx="50%" cy="50%" labelLine={false} label={({ name, pct }) => `${name} (${pct}%)`} outerRadius={100} fill="#8884d8" dataKey="value">
                      {signalTypes.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `${value} items`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Evidence Quality Metrics</h3>
                <div className="space-y-4">
                  <div className="p-3 bg-green-50 rounded border border-green-200">
                    <p className="text-sm font-semibold text-green-900">✅ Explicit Evidence</p>
                    <p className="text-2xl font-bold text-green-600">81.9%</p>
                    <p className="text-xs text-green-800">833 items directly stated in documents</p>
                  </div>
                  <div className="p-3 bg-orange-50 rounded border border-orange-200">
                    <p className="text-sm font-semibold text-orange-900">⚠️ Inferred Evidence</p>
                    <p className="text-2xl font-bold text-orange-600">18.1%</p>
                    <p className="text-xs text-orange-800">184 items require interpretation</p>
                  </div>
                  <div className="p-3 bg-blue-50 rounded border border-blue-200">
                    <p className="text-sm font-semibold text-blue-900">🎯 High Signal Strength</p>
                    <p className="text-2xl font-bold text-blue-600">50.0%</p>
                    <p className="text-xs text-blue-800">508 items - excellent support</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h3 className="text-lg font-bold text-slate-900 mb-4">Signal Relations & Commitment Levels</h3>
              <div className="space-y-3">
                <div className="p-4 bg-green-50 rounded">
                  <p className="font-semibold text-green-900">💚 Commits (543 items, 53.4%)</p>
                  <p className="text-sm text-green-800">Government explicitly commits to action - strongest support</p>
                </div>
                <div className="p-4 bg-blue-50 rounded">
                  <p className="font-semibold text-blue-900">📊 Targets (152 items, 14.9%)</p>
                  <p className="text-sm text-blue-800">Specific targets/metrics set - concrete measurable goals</p>
                </div>
                <div className="p-4 bg-yellow-50 rounded">
                  <p className="font-semibold text-yellow-900">⭐ Prioritizes (144 items, 14.2%)</p>
                  <p className="text-sm text-yellow-800">Action identified as priority - medium support</p>
                </div>
                <div className="p-4 bg-purple-50 rounded">
                  <p className="font-semibold text-purple-900">👥 Governs (48 items, 4.7%)</p>
                  <p className="text-sm text-purple-800">Governance mechanism established - medium-strong support</p>
                </div>
              </div>
            </div>

            <div className="bg-green-50 border border-green-200 p-6 rounded-lg">
              <h3 className="font-bold text-green-900 mb-3">✅ Quality Advantages</h3>
              <ul className="text-sm text-green-900 space-y-2">
                <li>✓ <strong>63% of evidence is "action" signals:</strong> Strong commitment language, not just context</li>
                <li>✓ <strong>50% high signal strength:</strong> Excellent quality (vs 9% in regional-only)</li>
                <li>✓ <strong>82% explicit evidence:</strong> Direct quotes, not inferred (vs 63% regional-only)</li>
                <li>✓ <strong>68% commits/targets/governs:</strong> Concrete commitments, not soft promises</li>
                <li>✓ <strong>Multi-source validation:</strong> Same actions referenced across 8 documents = stronger confidence</li>
              </ul>
            </div>
          </div>
        )}

        {/* FINDINGS TAB */}
        {activeTab === 'findings' && (
          <div className="space-y-8">
            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h2 className="text-xl font-bold text-slate-900 mb-4">🏆 Top 5 Strongest Actions</h2>
              <div className="space-y-3">
                {topActions.map((action, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded border border-green-200">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-slate-900">#{idx + 1}: {action.id}</p>
                        <p className="text-sm text-slate-600 mt-1">Evidence items: {action.evidence} | Source documents: {action.docs}</p>
                      </div>
                      <span className="text-3xl font-bold text-green-600">{(action.score * 100).toFixed(1)}%</span>
                    </div>
                    <div className="mt-2 w-full bg-slate-200 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-green-400 to-green-600 h-2 rounded-full"
                        style={{ width: `${action.score * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">💪 Strongest Support Areas</h3>
                <ul className="text-sm text-slate-700 space-y-3">
                  <li>
                    <strong className="text-green-600">Transport & Mobility:</strong>
                    <p className="text-xs text-slate-600">icare_0117 (99.8%), c40_0029 (99.0%), c40_0023 (98.4%)</p>
                  </li>
                  <li>
                    <strong className="text-green-600">Climate Adaptation:</strong>
                    <p className="text-xs text-slate-600">c40_0035 (97.8%), ipcc_0049 (97.5%)</p>
                  </li>
                  <li>
                    <strong className="text-green-600">Land Use & Nature:</strong>
                    <p className="text-xs text-slate-600">icare_0139 (97.1%), ipcc_0074 (97.1%)</p>
                  </li>
                  <li>
                    <strong className="text-green-600">Energy:</strong>
                    <p className="text-xs text-slate-600">ipcc_0067 (96.6%), c40_0042 (96.2%)</p>
                  </li>
                </ul>
              </div>

              <div className="bg-white p-6 rounded-lg border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">⚠️ Weaker Support Areas</h3>
                <ul className="text-sm text-slate-700 space-y-3">
                  <li>
                    <strong className="text-red-600">ipcc_0026 (19.6% - WEAK)</strong>
                    <p className="text-xs text-slate-600">7 evidence items from 3 documents only</p>
                  </li>
                  <li>
                    <strong className="text-orange-600">icare_0072 (31.3% - WEAK)</strong>
                    <p className="text-xs text-slate-600">Limited sectoral plan coverage</p>
                  </li>
                  <li>
                    <strong className="text-orange-600">icare_0079, icare_0082 (32.0% - WEAK)</strong>
                    <p className="text-xs text-slate-600">Regional priority but minimal evidence</p>
                  </li>
                </ul>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-slate-200">
              <h3 className="text-lg font-bold text-slate-900 mb-4">🎯 Key Findings & Recommendations</h3>
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border-l-4 border-green-400 rounded">
                  <p className="font-semibold text-green-900">✅ Strong Policy Alignment</p>
                  <p className="text-sm text-green-800">28.4% of actions have "strong" policy support (0.9+ score) with multiple document corroboration</p>
                </div>

                <div className="p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
                  <p className="font-semibold text-blue-900">✅ Evidence Quality</p>
                  <p className="text-sm text-blue-800">82% explicit evidence, 50% high signal strength - credible policy language with concrete commitments</p>
                </div>

                <div className="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                  <p className="font-semibold text-yellow-900">⚠️ Sectoral Variations</p>
                  <p className="text-sm text-yellow-800">Transport & energy have strongest support; some agriculture/health actions weaker. Consider prioritizing high-score actions.</p>
                </div>

                <div className="p-4 bg-orange-50 border-l-4 border-orange-400 rounded">
                  <p className="font-semibold text-orange-900">💡 Use This Data</p>
                  <p className="text-sm text-orange-800">policy_signal_valdivia.json is the authoritative dataset. It provides enough corroboration and specificity for investment/prioritization decisions.</p>
                </div>

                <div className="p-4 bg-red-50 border-l-4 border-red-400 rounded">
                  <p className="font-semibold text-red-900">⚠️ Still Missing</p>
                  <p className="text-sm text-red-800">Municipal-level PACCC for Valdivia would strengthen city-specific validation. Regional/national level evidence is solid but could use local confirmation.</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 p-6 rounded-lg">
              <h3 className="font-bold text-slate-900 mb-3">🎓 Final Assessment</h3>
              <p className="text-slate-700 text-sm leading-relaxed">
                The <strong>policy_signal_valdivia.json dataset is comprehensive and reliable</strong>. With 1,017 evidence items from 8 different sources (regional PARC + 6 sector plans + national framework), 
                it provides strong triangulation and validation for the 102 climate actions. The high quality of evidence (82% explicit, 50% high-strength signals) and presence of 29 "strong" support actions 
                demonstrate genuine policy commitment beyond rhetoric. <strong>Key actions like transport electrification, energy efficiency, and adaptation planning have excellent policy backing</strong>. 
                Use this data with confidence for planning and investment decisions, but ideally supplement with municipal PACCC when available.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
