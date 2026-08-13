from typing import Any

import unrealsdk

from mods_base import build_mod, hook
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct


@hook("WillowGame.WillowPawn:TakeDamage", Type.PRE)
def take_damage(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    try:
        if obj.IsPlayerPawn():
            return
    except Exception:
        pass

    try:
        hit_info = args.HitInfo

        hit_region = obj.GetHitRegionForTakenDamage(args.InstigatedBy, HitInfo=hit_info)

        if hit_region is None:
            return Block

        is_critical = bool(hit_region.bCriticalHit)

        if is_critical:
            return

        region_name = str(hit_region.Name)

        # debug
        #print("BONE:", hit_info.BoneName, "| REGION:", region_name, "| CRITICAL:", is_critical)

        # Engineer with helmet
        if region_name == "HitRegion_HeadArmor":
            return
        
        # Goliath with helmet
        if region_name == "HitRegion_Helmet":
            return
        
        return Block



    except Exception as e:
        print("HIT REGION ERROR:", repr(e))
        return Block


build_mod()