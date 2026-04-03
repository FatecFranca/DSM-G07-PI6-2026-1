import type { FunctionalComponent, HTMLAttributes, VNodeProps } from 'vue'

export interface Link {
  name: string
  icon: FunctionalComponent<HTMLAttributes & VNodeProps, {}, any>
  route: string
  disabled: boolean
}

export type Icon = FunctionalComponent<HTMLAttributes & VNodeProps, {}, any>;