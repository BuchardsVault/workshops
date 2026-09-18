import { useEffect, useState } from 'react'
import { apiFetch } from '../api'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'

/* How many rows to show before the card needs expanding */
const PREVIEW_COUNT = 5

/* The two that take money out of this account */
const OUTGOING = new Set(['WITHDRAW', 'TRANSFEROUT'])

const TYPE_LABELS = {
    DEPOSIT: 'Deposit',
    WITHDRAW: 'Withdrawal',
    TRANSFERIN: 'Transfer in',
    TRANSFEROUT: 'Transfer out',
}

function AccountCard({ account }) {
    const [transactions, setTransactions] = useState(null)
    const [expanded, setExpanded] = useState(false)

    useEffect(() => {
        async function loadTransactions() {
            try {
                setTransactions(
                    await apiFetch(`/api/accounts/${account.accountId}/transactions`)
                )
            } catch {
                /* Leave it null: the card still shows the balance and type */
            }
        }
        loadTransactions()
    }, [account.accountId])

    if (!account) return null

    /* The API sorts newest first, so the last entry is the oldest */
    const oldestTransaction = transactions?.[transactions.length - 1] ?? null
    const daysOpen = oldestTransaction ? daysSince(oldestTransaction.date) : null

    const visible = expanded
        ? transactions
        : transactions?.slice(0, PREVIEW_COUNT)
    const hiddenCount = (transactions?.length ?? 0) - PREVIEW_COUNT

    return (
        <Card className="text-left">
            <CardHeader>
                <CardDescription>Account #{account.accountId}</CardDescription>
                <CardTitle className="text-3xl tabular-nums">
                    ${Number(account.balance).toFixed(2)}
                </CardTitle>
                <CardAction>
                    <Badge variant="secondary">{account.accountType}</Badge>
                </CardAction>
            </CardHeader>

            <CardContent className="space-y-4">
                <p className="text-muted-foreground text-sm">
                    {daysOpen !== null
                        ? `Open for ${daysOpen} day${daysOpen === 1 ? '' : 's'} (approx.)`
                        : 'Days open unknown'}
                </p>

                <div className="space-y-2">
                    <p className="text-sm font-medium">Recent activity</p>

                    {transactions === null && (
                        <p className="text-muted-foreground text-sm">
                            Loading activity...
                        </p>
                    )}

                    {transactions?.length === 0 && (
                        <p className="text-muted-foreground text-sm">
                            No transactions yet
                        </p>
                    )}

                    {visible?.length > 0 && (
                        <ul className="divide-border divide-y text-sm">
                            {visible.map((txn, i) => {
                                const out = OUTGOING.has(txn.type)
                                return (
                                    <li
                                        key={i}
                                        className="flex items-baseline justify-between gap-3 py-2"
                                    >
                                        <span className="flex flex-col">
                                            <span>
                                                {TYPE_LABELS[txn.type] ?? txn.type}
                                            </span>
                                            <span className="text-muted-foreground text-xs">
                                                {formatDate(txn.date)}
                                            </span>
                                        </span>
                                        <span
                                            className={`shrink-0 tabular-nums ${
                                                out ? 'text-destructive' : 'text-emerald-600'
                                            }`}
                                        >
                                            {out ? '−' : '+'}$
                                            {Number(txn.amount).toFixed(2)}
                                        </span>
                                    </li>
                                )
                            })}
                        </ul>
                    )}

                    {hiddenCount > 0 && (
                        <Button
                            variant="link"
                            className="h-auto p-0 text-sm"
                            onClick={() => setExpanded((prev) => !prev)}
                        >
                            {expanded
                                ? 'Show less'
                                : `Show ${hiddenCount} more`}
                        </Button>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}

/* Transaction dates come as "YYYY-MM-DD HH:MM:SS". Returns null rather than
   throwing when a row arrives without one. */
function parseDate(dateStr) {
    if (typeof dateStr !== 'string') return null
    const [datePart, timePart = ''] = dateStr.split(' ')
    const [year, month, day] = datePart.split('-').map(Number)
    if (!year || !month || !day) return null
    const [hour = 0, minute = 0] = timePart.split(':').map(Number)
    return new Date(year, month - 1, day, hour, minute)
}

function daysSince(dateStr) {
    const date = parseDate(dateStr)
    if (!date) return null
    return Math.floor((Date.now() - date.getTime()) / (1000 * 60 * 60 * 24))
}

function formatDate(dateStr) {
    const date = parseDate(dateStr)
    if (!date) return 'Date unknown'
    return date.toLocaleString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
    })
}

export default AccountCard
