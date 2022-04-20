"use strict";

// payers. Could be expanded, however it is outside the scope of the microservice
const payers = ["DANNON", "UNILEVER", "MILLER COORS"];

const RedeemPoints = () => {
  return (
    <React.Fragment>
      <h3>Redeem Your Points</h3>
    </React.Fragment>
  );
};

const SpendPoints = () => {
  return (
    <React.Fragment>
      <h3>Spend Your Points</h3>
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
        backgroundColor: "rgba(255, 255, 255, 0.5)",
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
            <SpendPoints />
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<PointsContainer />, document.getElementById("root"));
