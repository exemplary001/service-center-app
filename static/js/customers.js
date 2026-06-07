function calculatePending() {

    let totalCalls =
        parseInt(
            document.getElementById(
                "total_calls"
            ).value
        ) || 0;

    let closedCalls =
        parseInt(
            document.getElementById(
                "closed_calls"
            ).value
        ) || 0;

    let pendingCalls =
        totalCalls - closedCalls;

    document.getElementById(
        "pending_calls"
    ).value = pendingCalls;
}


window.onload = function () {

    calculatePending();

};