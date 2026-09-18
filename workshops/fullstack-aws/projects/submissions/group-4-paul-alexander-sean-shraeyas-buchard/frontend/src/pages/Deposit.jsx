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

/* puts money in of one of the signed-in user's own accounts. */
function Deposit() {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState(null);
  const [accountId, setAccountId] = useState("");
  const [amount, setAmount] = useState("");

  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  /* The API only lets you touch your own accounts, so the picker is built
     from my-accounts rather than a free-typed id. */
  useEffect(() => {
    async function loadAccounts() {
      try {
        const mine = await apiFetch("/api/accounts/my-accounts");
        setAccounts(mine);
        if (mine.length > 0) setAccountId(String(mine[0].accountId));
      } catch (err) {
        setError(err.message);
        setAccounts([]);
      }
    }
    loadAccounts();
  }, []);

  const selected =
    accounts?.find((acc) => String(acc.accountId) === accountId) ?? null;

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setSubmitting(true);
    try {
      /* Amount goes over as a string so the decimal is not run through a
         float on the way out; pydantic parses it straight into a Decimal. */
      const res = await apiFetch(`/api/accounts/${accountId}/deposit`, {
        method: "POST",
        body: JSON.stringify({ amount: amount.trim() }),
      });
      setResult(res);
      setAmount("");

      /* Patch the returned balance in so the picker stays honest without a
         second round trip. */
      setAccounts((prev) =>
        prev.map((acc) =>
          acc.accountId === res.accountId
            ? { ...acc, balance: res.balance }
            : acc,
        ),
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
          You do not have an account to deposit in yet.
        </p>
        <Button asChild>
          <Link to="/accounts/new">Open an account</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-md">
      <Card className="text-left">
        <CardHeader>
          <CardTitle>Deposit</CardTitle>
          <CardDescription>
            Move money in of one of your accounts.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <p className="text-sm font-medium">To</p>
              <Select value={accountId} onValueChange={setAccountId}>
                <SelectTrigger className="w-full" aria-label="Account">
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
              {selected && (
                <p className="text-muted-foreground text-sm">
                  Available: ${Number(selected.balance).toFixed(2)}
                </p>
              )}
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
                Deposit. Account #{result.accountId} now holds $
                {Number(result.balance).toFixed(2)}.
              </p>
            )}

            <div className="flex gap-3">
              <Button type="submit" disabled={submitting}>
                {submitting ? "Depositing…" : "Deposit"}
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

export default Deposit;
