# Mintlayer Calculate Staking rewards Python Script

## Overview

This script processes staking data from a JSON file containing pool details, calculates balances and rewards, and outputs a summary of staking data in JSON format. It uses `MintLayerApiStrategy` and `MintLayerV2Api` for interacting with MintLayer APIs and leverages on coinmarketcap for upto date Mintlayer price.

---

## Prerequisites

1. **Python Version**: Ensure you have Python 3.7 or higher installed.
2. **Dependencies**:
   - `pydash`: For functional programming utilities.
   - Custom modules:
     - `api` containing:
       - `MintLayerApiStrategy`
       - `MintLayerV2Api`
     - `rw_stakemodel` containing:
       - `StakingData`
       - `Pool`

Install the required libraries using:

```bash
pip install pydash
```

---

## File Structure

```plaintext
.
├── pools.json          # Input file containing pool details
├── api.py              # API interactions module
├── rw_stakemodel.py    # Data models for staking
└── app.py           # The main script file
```

---

## Input

The script expects an input file named `pools.json` in the same directory. The file should contain an array of staking pools with the following structure:

```json
[
  {
    "pool_id": "string",
    "delegation_id": "string",
    "pool_balance": float,
    "delegation_datetime": "string"
  }
]
```

---

## Output

The script calculates the following metrics:
1. **MintLayer Coin Price** (`ml_price`): Retrieved from the MintLayer API.
2. **Total Staked Balance**: The sum of all delegation balances.
3. **Total Staked Rewards**: The sum of rewards for all pools.
4. **Total Pool Balance**: The sum of all pool balances.
5. **Total Staked Rewards Amount**: Rewards in monetary value.
6. **Staking Pools**: Detailed breakdown of each pool.

The results are printed as a JSON object with the following structure:

```json
{
    "ml_price": float,
    "total_staked_balance_amount": float,
    "total_staked_rewards": float,
    "total_staked_balance": float,
    "total_pool_balance": float,
    "total_staked_rewards_amount": float,
    "staking_pools": [
        {
            "pool_id": "string",
            "pool_balance": float,
            "delegation_id": "string",
            "delegation_datetime": "string",
            "delegation_balance": float,
            "pool_rewards": float,
            "ml_amount": float
        }
    ]
}
```

---

## Execution

1. Ensure the input file `pools.json` is correctly formatted and present.
2. Run the script:

   ```bash
   python app.py
   ```

3. The script outputs the calculated data in a pretty-printed JSON format to the console.

---

## Key Functions and Logic

- **MintLayer API Integration**:
  - Retrieves the current coin price using `ml_api.get_coin_price`.
  - Fetches `pool_balance` and `delegation_balance` for each pool.

- **Reward Calculation**:
  - Pool rewards: `delegation_balance - pool_balance` (if delegation balance is positive).
  - Monetary value of rewards: `pool_rewards * ml_price`.

- **Aggregation**:
  - Total staked balance, total pool balance, and reward amounts are summed across all pools.

---

