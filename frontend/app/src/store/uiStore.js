import { create } from 'zustand';
export const useUI = create(set => ({ tab: 'overview', setTab: tab => set({ tab }) }));
