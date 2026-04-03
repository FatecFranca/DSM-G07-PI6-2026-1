export interface Pet {
  id: string
  name: string
  species: 'DOG' | 'CAT' | 'BIRD' | 'RODENT' | 'REPTILE' | 'OTHER'
  breed: string
  color: string
  color_2: string | null
  gender: 'FEMALE' | 'MALE' | null
  spayed_neutered: boolean
  has_photo: boolean
  age: number
  weight: {
    value: number
    is_metric: number
  }
  is_removed: boolean
}

export type PetCondition =
  | 'Allergies or Food Sensitivities'
  | 'Digestive issues'
  | 'Dental issues'
  | 'Mobility concerns'
  | 'Overweight'
  | 'Urinary problems'
  | 'Skin/Coat problems'
