module FSOTScalarKernel

open FStar.Real
open FStar.Math.Exp

assume val cos : real -> real
assume val sin : real -> real
assume val sqrt : x:real{x >=. 0.0R} -> real

/// Host + bare-metal POC constants (mirrors verification/rust/fsot_scalar_kernel).
let k_fsot : real = 0.4202216641606967R
let alpha_fsot : real = 0.0008082937414140405R
let psi_con : real = 0.6321205588285577R
let eta_eff : real = 0.46694220692425986R
let beta_fsot : real = 0.00000000000000002620866911333223R
let c_eff : real = 0.9577022026205613R
let a_bleed : real = 1.046973630587551R
let b_in : real = 0.7879407922764435R
let a_in : real = 1.6668538450045731R
let chaos_fsot : real = 0.0R -. 0.33102418261048183R
let p_new : real = 0.30030227667037146R
let c_factor : real = 0.28760015181918397R
let poof : real = 0.1534822148944508R
let theta_s : real = 0.29089654054517305R
let suction : real = 0.14703398542810284R
let p_var : real = 0.9579871226722757R
let gamma_euler : real = 0.5772156649R
let phi_fsot : real = 1.6180339887R
let pi_fsot : real = 3.141592653589793R

let boot_d_eff : real = 8.0R
let boot_delta_psi : real = 0.7R
let boot_recent_hits : real = 0.0R
let boot_scalar_canonical : real = 0.09928895626861721R

/// Simplified S_D_chaotic POC (T2 = 0), matching rust_lean_bridge no_std kernel.
let compute_fsot_scalar (d_eff delta_psi: real) (observed: bool) (recent_hits: real) : real =
  let n = 1.0R in
  let p = 1.0R in
  let d = if d_eff <. 1.0R then 1.0R else d_eff in
  let dp = delta_psi in
  let hits = recent_hits in
  let growth = exp (alpha_fsot *. (1.0R -. hits /. n) *. gamma_euler /. phi_fsot) in
  let base =
    (n *. p /. sqrt d)
    *. cos ((psi_con +. dp) /. eta_eff)
    *. exp ((0.0R -. alpha_fsot) *. hits /. n +. 1.0R +. b_in *. dp)
    *. (1.0R +. growth *. c_eff)
  in
  let t1_base = base *. (1.0R +. p_new *. log (d /. 25.0R)) in
  let t1 =
    if observed
    then t1_base *. exp (c_factor *. p_var) *. cos (dp +. p_var)
    else t1_base
  in
  let t2 = 0.0R in
  let valve =
    beta_fsot *. cos dp *. (n *. p /. sqrt d)
    *. (1.0R +. chaos_fsot *. (d -. 25.0R) /. 25.0R)
    *. (1.0R +. poof *. cos (theta_s +. pi_fsot) +. suction *. sin theta_s)
  in
  let acoustic =
    1.0R
    +. (a_bleed *. (sin 1.0R) *. (sin 1.0R)) /. phi_fsot
    +. (a_in *. (cos 1.0R) *. (cos 1.0R)) /. phi_fsot
  in
  let phase = 1.0R +. b_in *. p_var in
  let t3 = valve *. acoustic *. phase in
  k_fsot *. (t1 +. t2 +. t3)

/// Runtime boot readout — delegated to FSOTScalarBoot (oracle-aligned at POC params).
let boot_scalar_kernel () : real =
  compute_fsot_scalar boot_d_eff boot_delta_psi true boot_recent_hits