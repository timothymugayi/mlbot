from typing import List

from pydantic import BaseModel


class Pool(BaseModel):
    pool_id: str
    delegation_id: str
    delegation_datetime: str
    pool_balance: float = 0.0
    pool_rewards: float = 0.0
    ml_amount: float = 0.0


class StakingData(BaseModel):
    ml_price: float
    total_pool_balance: float
    total_staked_balance: float
    total_staked_balance_amount: float
    total_staked_rewards_amount: float
    total_staked_rewards: float
    staking_pools: List[Pool]
