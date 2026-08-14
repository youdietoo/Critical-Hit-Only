from typing import Any

import unrealsdk

from mods_base import build_mod, hook
from unrealsdk.hooks import Type, Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct


@hook("WillowGame.WillowPawn:TakeDamage", Type.PRE)
def take_damage(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    instigator_con = args.InstigatedBy
    victim_pawn = obj
    
    # enemy vs enemy (eg: goliath vs any)
    try:
        if not victim_pawn.IsPlayerPawn() and not instigator_con.Pawn.IsPlayerPawn():
            return
    except Exception:
        pass
    
    # player should absolutely get damaged
    try:
        if victim_pawn.IsPlayerPawn():
            return
    except Exception:
        pass

    try:
        hit_info = args.HitInfo
        hit_region = victim_pawn.GetHitRegionForTakenDamage(instigator_con, HitInfo=hit_info)
        region_name = str(hit_region.Name)
        bone_name = str(hit_info.BoneName)
        
        # It can happen
        if hit_region is None:
            return Block
        
        is_critical = bool(hit_region.bCriticalHit)
        if is_critical:
            return
        
        # Engineer with helmet
        if region_name == "HitRegion_HeadArmor":
            return
        
        # Goliath with helmet
        if region_name == "HitRegion_Helmet":
            return
        
        # Midget Goliath because it has no critical spots
        if region_name == "HitRegion_Helmet_GoliathMidget":
            return
        
        # Turret (Hopefully...)
        if region_name == "HitRegion_Body" and bone_name == "MainGun":
            return
                
        # debug
        #print("BONE:", bone_name, "| REGION:", region_name, "| CRITICAL:", is_critical)
        
        return Block

    except Exception as e:
        print("HIT REGION ERROR:", repr(e))
        return Block


build_mod()
