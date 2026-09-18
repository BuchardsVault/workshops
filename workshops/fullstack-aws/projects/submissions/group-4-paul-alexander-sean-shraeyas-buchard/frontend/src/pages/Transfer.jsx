import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

/* Moves money from one of the signed-in user's accounts to any other
   account. Only the source is ownership-checked by the API, so the
   destination is typed in rather than picked. */
function Transfer() {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState(null);
  const [fromAccountId, setFromAccountId] = useState("");
  const [toAccountId, setToAccountId] = useState("");
  const [amount, setAmount] = useState("");

  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function loadAccounts() {
      try {
        const mine = await apiFetch("/api/accounts/my-accounts");
        setAccounts(mine);
        if (mine.length > 0) setFromAccountId(String(mine[0].accountId));
      } catch (err) {
        setError(err.message);
        setAccounts([]);
      }
    }
    loadAccounts();
  }, []);

  const source =
    accounts?.find((acc) => String(acc.accountId) === fromAccountId) ?? null;

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setSubmitting(true);
    try {
      /* toAccountId is an int in the schema so it goes as a number, while
         amount stays a string to keep the decimal exact. */
      const res = await apiFetch(`/api/accounts/${fromAccountId}/transfer`, {
        method: "POST",
        body: JSON.stringify({
          toAccountId: Number(toAccountId),
          amount: amount.trim(),
        }),
      });
      setResult(res);
      setAmount("");

      /* The response carries both balances. Patch whichever of them are
         ours; the destination often belongs to somebody else. */
      setAccounts((prev) =>
        prev.map((acc) => {
          if (acc.accountId === res.sourceAccountId)
            return { ...acc, balance: res.sourceBalance };
          if (acc.accountId === res.targetAccountId)
            return { ...acc, balance: res.targetBalance };
          return acc;
        }),
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (accounts === null) {
    return <p className="text-muted-foreground">Loading accounts...</p>;
  }

  if (accounts.length === 0) {
    return (
      <div className="mx-auto max-w-md space-y-4">
        <p className="text-muted-foreground">
          You do not have an account to transfer from yet.
        </p>
        <Button asChild>
          <Link to="/accounts/new">Open an account</Link>
        </Button>
      </div>
    );
  }

  /* Only echo the destination balance back when it is an account of ours */
  const targetIsMine =
    result && accounts.some((acc) => acc.accountId === result.targetAccountId);

  return (
    <div className="mx-auto max-w-md">
      <Card className="text-left">
        <CardHeader>
          <CardTitle>Transfer</CardTitle>
          <CardDescription>
            Send money to one of your own accounts or to someone else's.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <p className="text-sm font-medium">From</p>
              <Select value={fromAccountId} onValueChange={setFromAccountId}>
                <SelectTrigger className="w-full" aria-label="From account">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {accounts.map((acc) => (
                    <SelectItem key={acc.accountId} value={String(acc.accountId)}>
                      {acc.accountType} #{acc.accountId} — $
                      {Number(acc.balance).toFixed(2)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {source && (
                <p className="text-muted-foreground text-sm">
                  Available: ${Number(source.balance).toFixed(2)}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="toAccountId">
                To account
              </label>
              <Input
                id="toAccountId"
                type="number"
                inputMode="numeric"
                step="1"
                min="1"
                value={toAccountId}
                onChange={(e) => setToAccountId(e.target.value)}
                placeholder="Account number"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="amount">
                Amount
              </label>
              <Input
                id="amount"
                type="number"
                inputMode="decimal"
                step="0.01"
                min="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                required
              />
            </div>

            {error && <p className="text-destructive text-sm">{error}</p>}

            {result && (
              <p className="text-sm">
                Sent to account #{result.targetAccountId}. Account #
                {result.sourceAccountId} now holds $
                {Number(result.sourceBalance).toFixed(2)}
                {targetIsMine &&
                  `, and #${result.targetAccountId} holds $${Number(
                    result.targetBalance,
                  ).toFixed(2)}`}
                .
              </p>
            )}

            <div className="flex gap-3">
              <Button type="submit" disabled={submitting}>
                {submitting ? "Sending…" : "Send transfer"}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/dashboard")}
              >
                Back to dashboard
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

export default Transfer;
