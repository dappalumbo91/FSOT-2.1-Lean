/-
  Chemical connection → D_eff (v15), Mathlib-backed Nat facts.
  Mirrors scripts/full_scalar_law.py chem_link_domain.
-/
import Mathlib.Tactic
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Card
import FSOTGenetics.Seeds

namespace FSOTGenetics

/-- Connecting chemical systems on the fold path. -/
inductive ChemLink where
  | backbone
  | disulfide
  | saltBridge
  | hydrophobicPack
  | hbondSecondary
  | molecularSidechain
  | tertiaryBiochem
  deriving DecidableEq, Repr, Fintype

/-- Pin-table domain names used by genetics fold. -/
inductive DomainName where
  | physicalChemistry
  | atomicPhysics
  | electromagnetism
  | condensedMatter
  | chemistry
  | molecularChemistry
  | biochemistry
  deriving DecidableEq, Repr, Fintype

/-- Effective dimension from the 35-domain pin table (Nat, not free). -/
def DomainName.D_eff : DomainName → Nat
  | .physicalChemistry  => 8
  | .atomicPhysics      => 7
  | .electromagnetism   => 9
  | .condensedMatter    => 14
  | .chemistry          => 8
  | .molecularChemistry => 9
  | .biochemistry       => 13

/-- Chem link → domain (connecting systems / interacting chemistry). -/
def ChemLink.domain : ChemLink → DomainName
  | .backbone           => .physicalChemistry
  | .disulfide          => .atomicPhysics
  | .saltBridge         => .electromagnetism
  | .hydrophobicPack    => .condensedMatter
  | .hbondSecondary     => .chemistry
  | .molecularSidechain => .molecularChemistry
  | .tertiaryBiochem    => .biochemistry

def ChemLink.D_eff (c : ChemLink) : Nat := c.domain.D_eff

-- ── Locked D_eff facts (must match Python chem_link_domain) ─────────────

theorem backbone_D : ChemLink.backbone.D_eff = 8 := by rfl
theorem disulfide_D : ChemLink.disulfide.D_eff = 7 := by rfl
theorem salt_D : ChemLink.saltBridge.D_eff = 9 := by rfl
theorem hydro_pack_D : ChemLink.hydrophobicPack.D_eff = 14 := by rfl
theorem hbond_D : ChemLink.hbondSecondary.D_eff = 8 := by rfl
theorem molecular_D : ChemLink.molecularSidechain.D_eff = 9 := by rfl
theorem tertiary_D : ChemLink.tertiaryBiochem.D_eff = 13 := by rfl

/-- All protein chem-link D_eff values sit in the pin ladder [pinDMin, pinDMax]. -/
theorem chem_link_D_in_pin_range (c : ChemLink) :
    pinDMin ≤ c.D_eff ∧ c.D_eff ≤ pinDMax := by
  cases c <;> decide

theorem salt_not_backbone_D :
    ChemLink.saltBridge.D_eff ≠ ChemLink.backbone.D_eff := by decide

theorem pack_not_tertiary_D :
    ChemLink.hydrophobicPack.D_eff ≠ ChemLink.tertiaryBiochem.D_eff := by decide

theorem disulfide_not_molecular_D :
    ChemLink.disulfide.D_eff ≠ ChemLink.molecularSidechain.D_eff := by decide

/-- Hydrophobic packing is a *higher* dimensional interface than molecular sidechain. -/
theorem pack_D_gt_molecular :
    ChemLink.molecularSidechain.D_eff < ChemLink.hydrophobicPack.D_eff := by decide

/-- Tertiary biochem interface is above backbone geometry. -/
theorem tertiary_D_gt_backbone :
    ChemLink.backbone.D_eff < ChemLink.tertiaryBiochem.D_eff := by decide

/-- Disulfide (atomic) is below condensed packing. -/
theorem disulfide_D_lt_pack :
    ChemLink.disulfide.D_eff < ChemLink.hydrophobicPack.D_eff := by decide

/-- There are exactly 7 chem-link classes. -/
theorem chemLink_card : Fintype.card ChemLink = 7 := by
  native_decide

/-- Image of D_eff over all chem links is a finite set of pin dimensions. -/
def chemLinkDSet : Finset Nat :=
  Finset.image ChemLink.D_eff Finset.univ

theorem chemLinkDSet_subset_pin :
    ∀ d ∈ chemLinkDSet, pinDMin ≤ d ∧ d ≤ pinDMax := by
  intro d hd
  rcases Finset.mem_image.mp hd with ⟨c, _, rfl⟩
  exact chem_link_D_in_pin_range c

end FSOTGenetics
