import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getCurrentUser } from '../currentUser'
import { apiFetch } from '../api'
import { Button } from '@/components/ui/button'
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

const ACCOUNT_TYPES = [
    { value: 'CHECKING', label: 'Checking' },
    { value: 'SAVINGS', label: 'Savings' },
]

/* Opens another account for whoever is already signed in. */
function NewAccount() {
    const navigate = useNavigate()
    const user = getCurrentUser()
    const [accountType, setAccountType] = useState(ACCOUNT_TYPES[0].value)
    const [error, setError] = useState(null)
    const [submitting, setSubmitting] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault()
        setError(null)
        setSubmitting(true)
        try {
            /* The API wants the owner in the body and compares it against the
               token, so this has to be the signed-in user's own id. */
            await apiFetch('/api/accounts', {
                method: 'POST',
                body: JSON.stringify({ userId: user.userId, accountType }),
            })
            navigate('/dashboard')
        } catch (err) {
            setError(err.message)
        } finally {
            setSubmitting(false)
        }
    }

    /* AppLayout already guards this route; this is just so the submit
       handler can never read userId off null. */
    if (!user) return <p className="text-muted-foreground">Not signed in.</p>

    return (
        <div className="mx-auto max-w-md">
            <Card className="text-left">
                <CardHeader>
                    <CardTitle>Open a new account</CardTitle>
                    <CardDescription>
                        New accounts start with a balance of $0.00.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div className="space-y-2">
                            <p className="text-sm font-medium">Account type</p>
                            <Select value={accountType} onValueChange={setAccountType}>
                                <SelectTrigger className="w-full" aria-label="Account type">
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    {ACCOUNT_TYPES.map(({ value, label }) => (
                                        <SelectItem key={value} value={value}>
                                            {label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        {error && <p className="text-destructive text-sm">{error}</p>}

                        <div className="flex gap-3">
                            <Button type="submit" disabled={submitting}>
                                {submitting ? 'Opening…' : 'Open account'}
                            </Button>
                            <Button
                                type="button"
                                variant="outline"
                                onClick={() => navigate('/dashboard')}
                            >
                                Cancel
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}

export default NewAccount
