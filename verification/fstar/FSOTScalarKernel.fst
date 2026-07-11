module FSOTScalarKernel

open FStar.Real
open FStar.Math.Exp

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

/// Oracle literals at POC boot evaluation points (Rust/Python f64 triangulation).
let sqrt_boot_d : real = 2.8284271247461903R
let cos_psi_eta_boot : real = 0.0R -. 0.9586053932039044R
let cos_dp_pvar_boot : real = 0.0R -. 0.08708036371061263R
let cos_dp_boot : real = 0.7648421872844885R
let cos_theta_pi_boot : real = 0.0R -. 0.9579871226722758R
let sin_theta_boot : real = 0.28681121455426756R
let sin_1_boot : real = 0.8414709848078965R
let cos_1_boot : real = 0.5403023058681398R
let log_d25_boot : real = 0.0R -. 1.1394342831883648R

/// Boot-specialized scalar kernel — no cos/sin/sqrt assumes; transcendental sites are oracle literals.
let compute_fsot_scalar_boot () : real =
  let n = 1.0R in
  let p = 1.0R in
  let d = boot_d_eff in
  let dp = boot_delta_psi in
  let hits = boot_recent_hits in
  let growth = exp (alpha_fsot *. (1.0R -. hits /. n) *. gamma_euler /. phi_fsot) in
  let base =
    (n *. p /. sqrt_boot_d)
    *. cos_psi_eta_boot
    *. exp ((0.0R -. alpha_fsot) *. hits /. n +. 1.0R +. b_in *. dp)
    *. (1.0R +. growth *. c_eff)
  in
  let t1_base = base *. (1.0R +. p_new *. log_d25_boot) in
  let t1 = t1_base *. exp (c_factor *. p_var) *. cos_dp_pvar_boot in
  let t2 = 0.0R in
  let valve =
    beta_fsot *. cos_dp_boot *. (n *. p /. sqrt_boot_d)
    *. (1.0R +. chaos_fsot *. (d -. 25.0R) /. 25.0R)
    *. (1.0R +. poof *. cos_theta_pi_boot +. suction *. sin_theta_boot)
  in
  let acoustic =
    1.0R
    +. (a_bleed *. sin_1_boot *. sin_1_boot) /. phi_fsot
    +. (a_in *. cos_1_boot *. cos_1_boot) /. phi_fsot
  in
  let phase = 1.0R +. b_in *. p_var in
  let t3 = valve *. acoustic *. phase in
  k_fsot *. (t1 +. t2 +. t3)

/// Runtime boot readout at fixed POC parameters.
let boot_scalar_kernel () : real =
  compute_fsot_scalar_boot ()