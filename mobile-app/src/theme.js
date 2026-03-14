/**
 * Theme Configuration
 * Color-coded system for risk levels and UI elements
 */

export const Colors = {
  // Risk levels - traffic light system
  GREEN: '#10B981',      // Healthy - good breathing
  YELLOW: '#F59E0B',     // Warning - monitor closely
  RED: '#EF4444',        // Critical - seek medical attention

  // UI Colors
  WHITE: '#FFFFFF',
  LIGHT_GRAY: '#F3F4F6',
  GRAY: '#9CA3AF',
  DARK_GRAY: '#374151',
  DARK: '#1F2937',

  // Semantic colors
  SUCCESS: '#10B981',
  WARNING: '#F59E0B',
  ERROR: '#EF4444',
  INFO: '#3B82F6',

  // Background
  BACKGROUND: '#FFFFFF',
  SURFACE: '#F9FAFB',
};

export const Spacing = {
  xs: 8,
  sm: 12,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const Typography = {
  h1: {
    fontSize: 32,
    fontWeight: 'bold',
  },
  h2: {
    fontSize: 24,
    fontWeight: '600',
  },
  h3: {
    fontSize: 20,
    fontWeight: '600',
  },
  body: {
    fontSize: 16,
    fontWeight: '400',
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
  },
  small: {
    fontSize: 12,
    fontWeight: '400',
  },
};

export const RiskLevel = {
  HEALTHY: {
    color: Colors.GREEN,
    label: 'Healthy',
    description: 'Breathing looks good!',
    icon: '✓',
  },
  WARNING: {
    color: Colors.YELLOW,
    label: 'Monitor',
    description: 'Watch for changes',
    icon: '⚠',
  },
  CRITICAL: {
    color: Colors.RED,
    label: 'Check Now',
    description: 'Contact healthcare provider',
    icon: '⚠',
  },
};

export const BorderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  full: 9999,
};
