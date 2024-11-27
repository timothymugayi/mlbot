import json

from pydash import py_

from api import MintLayerApiStrategy, MintLayerV2Api
from rw_stakemodel import StakingData, Pool


ml_api = MintLayerApiStrategy(MintLayerV2Api)
ml_price = ml_api.get_coin_price()

file_path = 'pools.json'
with open(file_path, 'r') as file:
    pools = json.load(file)

total_staked_balance = 0.0
total_staked_rewards_amount = 0.0
total_staked_rewards = 0.0
staking_pools = []

for pool in pools:
    pool_balance = ml_api.get_pool_balance(pool.get("pool_id"))
    delegation_balance = ml_api.get_delegation_balance(pool.get("delegation_id"))
    total_staked_balance += delegation_balance
    pool_rewards = (delegation_balance - pool.get("pool_balance") if delegation_balance > 0 else 0)
    total_staked_rewards += pool_rewards
    ml_amount = (pool_rewards * ml_price if pool_rewards > 0 else 0)
    total_staked_rewards_amount += ml_amount
    staking_pools.append(
        Pool(pool_id=pool.get("pool_id"),
             pool_balance=pool_balance,
             delegation_id=pool.get("delegation_id"),
             delegation_datetime=pool.get("delegation_datetime"),
             delegation_balance=delegation_balance,
             pool_rewards=pool_rewards,
             ml_amount=ml_amount)
    )

total_pool_balance = py_.sum_by(pools, "pool_balance")
data = StakingData(
    ml_price=ml_price,
    total_staked_balance_amount=(total_staked_balance * ml_price),
    total_staked_rewards=total_staked_rewards,
    total_staked_balance=total_staked_balance,
    total_pool_balance=total_pool_balance,
    total_staked_rewards_amount=total_staked_rewards_amount,
    staking_pools=staking_pools)

print(json.dumps(data.dict(), sort_keys=True, indent=4))
