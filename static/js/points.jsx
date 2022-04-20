"use strict";

// payers. Could add to database, however it is outside the scope of the microservice
const payers = ["DANNON", "UNILEVER", "MILLER COORS"];

const RedeemPoints = () => {
  const [payer, setPayer] = React.useState("");
  const [points, setPoints] = React.useState(0);
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
      .then((response) => {
        response.json();
      })
      .then((jsonResponse) => {
        console.log(jsonResponse);
        props.getPointBalance();
      });
  };

  return (
    <React.Fragment>
      <h3>Redeem Your Points</h3>
    </React.Fragment>
  );
};

const SpendPoints = (props) => {
  const [points, setPoints] = React.useState(0);

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
      .then((response) => {
        response.json();
      })
      .then((jsonResponse) => {
        console.log(jsonResponse);
        props.getPointBalance();
      });
  };

  // Validate form - need to make sure to spend amount is less than points balance
  const validateSpend = () => {
    if (points >= props.balance || points === "" || points === "0") {
      alert(`You can spend up to ${props.balance} points. Please try again.`);
    } else {
      spendPoints();
    }
  };

  return (
    <React.Fragment>
      <h3>Spend Your Points</h3>
      <input
        type="number"
        step={1}
        min={0}
        className="form-control input-sm"
        onChange={(event) => setPoints(event.target.value)}
      />
      <button
        className="btn btn-sm btn-outline-dark btn-block"
        onClick={validateSpend}
      >
        Submit
      </button>
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
          <h2>Points: {points}</h2>
        </div>
        <div
          className="d-flex"
          style={{ height: "calc(100% - 50px)", width: "100%" }}
        >
          <div
            className="col-md-6 g-2"
            style={{ border: "1px solid black", height: "100%" }}
          >
            <RedeemPoints />
          </div>
          <div
            className="col-md-6 g-2"
            style={{ border: "1px solid black", height: "100%" }}
          >
            <SpendPoints balance={points} getPointBalance={getPointBalance} />
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<PointsContainer />, document.getElementById("root"));
