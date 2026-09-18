import { useState } from 'react'
import { apiFetch } from '../api'

function TransactionLookup() {
  const [accountId, setAccountId] = useState('')
  const [transactions, setTransactions] = useState([])
  const [error, setError] = useState(null)

  /* The API enforces ownership, so this only resolves for accounts
     belonging to whoever is signed in. */
  async function lookup(e) {
    e.preventDefault()
    setError(null)
    try {
      setTransactions(await apiFetch(`/api/accounts/${accountId}/transactions`))
    } catch (err) {
      setError(err.message)
      setTransactions([])
    }
  }

  return (
    <>
      <form onSubmit={lookup}>
        <input
          value={accountId}
          onChange={(e) => setAccountId(e.target.value)}
          placeholder="Account ID"
        />
        <button type="submit">Look up</button>
      </form>

      {error && <p>{error}</p>}

      <table>
        <thead>
          <tr><th>Type</th><th>Amount</th><th>Date</th></tr>
        </thead>
        <tbody>
          {transactions.map((t, i) => (
            <tr key={i}>
              <td>{t.type}</td>
              <td>{t.amount}</td>
              <td>{t.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export default TransactionLookup
