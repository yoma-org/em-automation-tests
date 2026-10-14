// src/utils/Environment.ts
import path from 'node:path';

export const roles = ['admin', 'uo-operator', 'uo-manager'] as const; // extend with the roles the suite uses
export type Role = (typeof roles)[number];

function required(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing env var ${name} (see .env.example)`);
  return value;
}

export const env = {
  get baseUrl() { return required('BASE_URL'); },
  get apiBaseUrl() { return required('API_BASE_URL'); },
  get partnerApiBaseUrl() { return required('PARTNER_API_BASE_URL'); },
  get apiPayloadKey() { return required('API_PAYLOAD_KEY'); }
};

// 'uo-operator' → UO_OPERATOR_EMAIL / UO_OPERATOR_PASSWORD
export function credentials(role: Role): { email: string; password: string } {
  const prefix = role.toUpperCase().replaceAll('-', '_');
  return { email: required(`${prefix}_EMAIL`), password: required(`${prefix}_PASSWORD`) };
}

export function authFile(role: Role): string {
  return path.join('playwright', '.auth', `${role}.json`);
}
