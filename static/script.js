// Train Model Function
async function trainModel() {
  const trainResult = document.getElementById("trainResult");
  trainResult.innerHTML = "Training model...";

  try {
    const response = await fetch("/train", {
      method: "POST",
    });
    const data = await response.json();

    if (response.ok) {
      trainResult.innerHTML = `
                <div class="alert-success">
                    <p>${data.message}</p>
                </div>`;
    } else {
      trainResult.innerHTML = `
                <div class="alert-danger">
                    Error: ${data.error}
                </div>`;
    }
  } catch (error) {
    trainResult.innerHTML = `
            <div class="alert-danger">
                Error: ${error.message}
            </div>`;
  }
}

// Predict Function
async function predict() {
  const predictResult = document.getElementById("predictResult");
  const feature1 = parseFloat(document.getElementById("feature1").value);
  const feature2 = parseFloat(document.getElementById("feature2").value);
  const feature3 = parseFloat(document.getElementById("feature3").value);

  if (isNaN(feature1) || isNaN(feature2) || isNaN(feature3)) {
    predictResult.innerHTML = `
            <div class="alert-danger">
                Please enter valid numbers for all features
            </div>`;
    return;
  }

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        feature1: feature1,
        feature2: feature2,
        feature3: feature3,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      let riskLevel = "Low";
      if (feature1 > 0.8 || feature2 > 0.8 || feature3 > 0.8) {
        riskLevel = "High";
      } else if (feature1 > 0.5 || feature2 > 0.5 || feature3 > 0.5) {
        riskLevel = "Medium";
      }

      predictResult.innerHTML = `
                <div class="prediction-box prediction-${data.prediction.toLowerCase()}">
                    <h3>Analysis Result:</h3>
                    <div class="prediction-result">
                        <strong>Status:</strong> ${data.prediction}
                        <div class="risk-level ${riskLevel.toLowerCase()}-risk">
                            <strong>Risk Level:</strong> ${riskLevel}
                        </div>
                        <div class="metrics">
                            <strong>Metrics:</strong>
                            <ul>
                                <li>Network Traffic: ${feature1}</li>
                                <li>CPU Usage: ${feature2}</li>
                                <li>Memory Usage: ${feature3}</li>
                            </ul>
                        </div>
                    </div>
                </div>`;
    } else {
      predictResult.innerHTML = `
                <div class="alert-danger">
                    Error: ${data.error}
                </div>`;
    }
  } catch (error) {
    predictResult.innerHTML = `
            <div class="alert-danger">
                Error: ${error.message}
            </div>`;
  }
}
