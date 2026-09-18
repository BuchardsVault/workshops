import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api";
import "../CreateAccount.css";

function CreateAccount() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      /* Registration is the one public endpoint. Opening an actual bank
         account happens later, from the dashboard, with a token. */
      await apiFetch("/api/users", {
        method: "POST",
        body: JSON.stringify({ name, email, password }),
      });
      navigate("/login");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div id="center">
      <div className="auth-card">
        <h1 className="auth-title">Create account</h1>
        <p className="auth-subtitle">
          Fill in your details to set up a new account.
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label className="field">
            <span>Name</span>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Jane Doe"
              autoComplete="name"
              required
            />
          </label>

          <label className="field">
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="jane@example.com"
              autoComplete="email"
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="new-password"
              required
            />
          </label>

          {error && <p className="form-error">{error}</p>}

          <div className="button-row">
            <button
              type="submit"
              className="primary-button"
              disabled={submitting}
            >
              {submitting ? "Creating account…" : "Confirm details"}
            </button>
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate("/login")}
            >
              Back to home
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateAccount;
