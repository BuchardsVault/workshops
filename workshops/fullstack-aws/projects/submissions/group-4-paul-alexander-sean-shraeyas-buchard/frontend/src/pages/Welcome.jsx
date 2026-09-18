import { useNavigate } from "react-router-dom";
import "../Welcome.css";
import welcomeBg from "../assets/welcome-bg.png";

function Welcome() {
  const navigate = useNavigate();

  return (
    <div
      className="welcome-view"
      style={{ "--welcome-bg-image": `url(${welcomeBg})` }}
    >
      <div className="welcome-content">
        <h1 className="welcome-title">Welcome to CHAD Banking</h1> 
        <p className="welcome-subtital">
          C.H.A.D = Can Handle A Dollar
        </p>
        <p className="welcome-subtitle">
          Manage your accounts, track transactions, and move money, all in one
          place.
        </p>
      </div>

      <div className="welcome-actions">
        <button
          type="button"
          className="primary-button"
          onClick={() => navigate("/login")}
        >
          Sign in
        </button>
        <button
          type="button"
          className="secondary-button"
          onClick={() => navigate("/signup")}
        >
          Create account
        </button>
      </div>
    </div>
  );
}

export default Welcome;
