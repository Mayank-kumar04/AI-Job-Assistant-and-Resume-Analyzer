import { useRef, useState } from 'react'
import { useSelection } from '../hooks/useSelection'
import { chatAPI, formatApiError } from '../services/api'

const SUGGESTIONS = [
  'Am I suitable for this role?',
  'What skills are missing?',
  'How can I improve my resume?',
  'What backend technologies should I learn?',
]

export default function AIChatbot() {
  const { resumeId, jdId, loading } = useSelection()
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        'Hi! Ask me anything about your resume and job description. I use RAG with Gemini AI.',
    },
  ])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)

  const send = async (question) => {
    if (!question.trim() || !resumeId) return

    setMessages((m) => [...m, { role: 'user', content: question }])
    setInput('')
    setSending(true)

    try {
      const { data } = await chatAPI.query({
        resume_id: parseInt(resumeId),
        jd_id: jdId ? parseInt(jdId) : null,
        question,
        session_id: sessionId,
      })

      setSessionId(data.session_id)

      setMessages((m) => [
        ...m,
        { role: 'assistant', content: data.answer },
      ])

      setTimeout(
        () => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }),
        100
      )
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: formatApiError(err) },
      ])
    } finally {
      setSending(false)
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col animate-slide-up">

      {/* Page Header */}
      <h2 className="text-3xl font-bold text-gray-100">
        AI Resume Assistant
      </h2>

      <p className="mt-2 text-gray-400">
        Context-aware answers from your resume & job description
      </p>

      {/* Suggestions */}
      <div className="mt-4 flex flex-wrap gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => send(s)}
            className="rounded-full border border-[#353b45] px-3 py-1 text-sm text-gray-300 transition hover:bg-[#252a32] hover:text-white"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Chat Box */}
      <div className="card mt-4 flex flex-1 flex-col overflow-hidden">

        <div className="flex-1 space-y-4 overflow-y-auto p-4">

          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === 'user'
                  ? 'justify-end'
                  : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap ${
                  msg.role === 'user'
                    ? 'bg-[#4f46e5] text-white'
                    : 'bg-[#20252d] text-gray-200'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          <div ref={bottomRef} />

        </div>

        {/* Input */}
        <div className="border-t border-[#2a2f38] p-4">

          <form
            onSubmit={(e) => {
              e.preventDefault()
              send(input)
            }}
            className="flex gap-3"
          >
            <input
              className="input-field flex-1"
              placeholder="Ask about your resume..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={sending}
            />

            <button
              type="submit"
              disabled={sending}
              className="btn-primary"
            >
              {sending ? '...' : 'Send'}
            </button>
          </form>

        </div>
      </div>
    </div>
  )
}