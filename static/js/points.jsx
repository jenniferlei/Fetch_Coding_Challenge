"use strict";

// Payer and Category options. Could expand and add to database, however it is outside the scope of the microservice
const payerOptions = ["DANNON", "UNILEVER", "MILLER COORS"];
const rewardCategoryOptions = [
  "Merch",
  "Sweepstakes",
  "Gift Card",
  "Cash Card",
  "Charity",
  "Travel",
  "Specialty",
];

const EarnPoints = (props) => {
  const [payer, setPayer] = React.useState("");
  const [points, setPoints] = React.useState("");
  const [timestamp, setTimestamp] = React.useState("");

  const addPoints = () => {
    fetch("/add_points.json", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        payer,
        points,
        timestamp,
      }),
    })
      .then((response) => response.json())
      .then((jsonResponse) => {
        console.log(jsonResponse);
        props.getPointBalance();
      });
  };

  const validateEarn = () => {
    const alertText = "Please complete the following:";
    const payerAlert = "\n• select a payer";
    const pointsAlert = "\n• input points";
    const timestampAlert = "\n• input timestamp";

    if (
      payer === "" ||
      points === "" ||
      Number(points) <= 0 ||
      timestamp === ""
    ) {
      let completeAlertText = [alertText];
      if (payer === "") {
        completeAlertText.push(payerAlert);
      }
      if (points === "" || Number(points) <= 0) {
        completeAlertText.push(pointsAlert);
      }
      if (timestamp === "") {
        completeAlertText.push(timestampAlert);
      }
      alert(completeAlertText.join(""));
    } else {
      addPoints();
    }
  };

  return (
    <React.Fragment>
      <h3>Earn Points</h3>
      Earn points by submitting the payer, number of points and timestamp from
      your receipt!
      <div className="mt-3">
        <label htmlFor="payer-input">Payer</label>
        <select
          id="payer-input"
          className="form-select"
          aria-label="payer-input"
          onChange={(event) => setPayer(event.target.value)}
        >
          <option value=""></option>
          {payerOptions.map((payerOption) => (
            <option value={payerOption}>{payerOption}</option>
          ))}
        </select>
      </div>
      <div className="mt-3">
        <label htmlFor="earn-points-input">Points Earned</label>
        <input
          id="earn-points-input"
          type="number"
          step={1}
          min={0}
          className="form-control input-sm"
          onChange={(event) => setPoints(event.target.value)}
        />
      </div>
      <div className="mt-3">
        <label htmlFor="timestamp-input">Timestamp</label>
        <input
          id="timestamp-input"
          type="datetime-local"
          onChange={(event) => setTimestamp(event.target.value)}
          className="form-control"
        />
      </div>
      <div className="mt-3">
        <button
          className="btn btn-sm btn-outline-dark btn-block"
          onClick={validateEarn}
        >
          Submit
        </button>
      </div>
    </React.Fragment>
  );
};

const SpendPoints = (props) => {
  const [points, setPoints] = React.useState("");

  const spendPoints = () => {
    fetch("/spend_points.json", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        points,
      }),
    })
      .then((response) => response.json())
      .then((jsonResponse) => {
        console.log(jsonResponse);
        props.getPointBalance();
      });
  };

  // Validate form - need to make sure to spend amount is less than points balance
  const validateSpend = () => {
    if (points >= props.balance) {
      alert(`You can spend up to a maximum of ${props.balance} points.`);
    } else if (points === "" || Number(points) <= 0) {
      alert("Please complete the following:\n• input points");
    } else {
      spendPoints();
    }
  };

  return (
    <React.Fragment>
      <h3>Spend Your Points</h3>
      Reward yourself with the points you've earned! Select a reward category
      and input how many points you would like to use.
      <div className="mt-3">
        <label htmlFor="reward-input">Reward Category</label>
        <select
          id="reward-input"
          className="form-select"
          aria-label="reward-input"
        >
          <option value=""></option>
          {rewardCategoryOptions.map((reward) => (
            <option value={reward}>{reward}</option>
          ))}
        </select>
      </div>
      <div className="mt-3">
        <label htmlFor="spend-points-input">Points</label>
        <input
          id="spend-points-input"
          type="number"
          step={1}
          min={0}
          className="form-control input-sm"
          onChange={(event) => setPoints(event.target.value)}
        />
      </div>
      <div className="mt-3">
        <button
          className="btn btn-sm btn-outline-dark btn-block"
          onClick={validateSpend}
        >
          Submit
        </button>
      </div>
    </React.Fragment>
  );
};

const PointsContainer = () => {
  const [points, setPoints] = React.useState("");

  React.useEffect(() => {
    getPointBalance();
  }, []);

  const getPointBalance = () => {
    fetch("/point_balance.json")
      .then((response) => response.json())
      .then((responseJson) => {
        let sum = 0;
        console.log(responseJson);
        for (const key in responseJson) {
          sum += responseJson[key];
        }
        setPoints(sum);
      });
  };

  return (
    <div
      className="card"
      style={{
        top: "1.5em",
        width: "90vw",
        height: "80vh",
        margin: "auto",
        backgroundColor: "rgba(255, 255, 255, 0.7)",
      }}
    >
      <div className="card-body">
        <div className="d-flex">
          <h2>Your Points: {points}</h2>
        </div>
        <div
          className="d-flex"
          style={{ height: "calc(100% - 50px)", width: "100%" }}
        >
          <div className="col-md-6 pe-2" style={{ height: "100%" }}>
            <EarnPoints balance={points} getPointBalance={getPointBalance} />
          </div>
          <div className="col-md-6 ps-2" style={{ height: "100%" }}>
            <SpendPoints balance={points} getPointBalance={getPointBalance} />
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<PointsContainer />, document.getElementById("root"));
