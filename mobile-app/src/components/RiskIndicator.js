/**
 * Risk Indicator Component
 * Large visual indicator for risk level (Green/Yellow/Red)
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors, RiskLevel, Spacing, BorderRadius, Typography } from '../theme';

export const RiskIndicator = ({ riskLevel, score, showDetails = true }) => {
  const riskConfig = getRiskConfig(riskLevel);

  const styles = StyleSheet.create({
    container: {
      alignItems: 'center',
      marginVertical: Spacing.lg,
    },
    indicator: {
      width: 180,
      height: 180,
      borderRadius: BorderRadius.full,
      backgroundColor: riskConfig.color,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: Spacing.lg,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.3,
      shadowRadius: 8,
      elevation: 8,
    },
    icon: {
      fontSize: 80,
      fontWeight: 'bold',
      color: Colors.WHITE,
      marginBottom: Spacing.sm,
    },
    label: {
      fontSize: 28,
      fontWeight: 'bold',
      color: riskConfig.color,
      marginBottom: Spacing.sm,
    },
    description: {
      fontSize: 16,
      color: Colors.DARK_GRAY,
      marginBottom: Spacing.sm,
    },
    scoreContainer: {
      marginTop: Spacing.md,
      alignItems: 'center',
    },
    scoreLabel: {
      fontSize: 12,
      color: Colors.GRAY,
      marginBottom: Spacing.xs,
    },
    scoreValue: {
      fontSize: 36,
      fontWeight: 'bold',
      color: riskConfig.color,
    },
    scoreUnit: {
      fontSize: 14,
      color: Colors.GRAY,
      marginLeft: Spacing.xs,
    },
  });

  return (
    <View style={styles.container}>
      <View style={styles.indicator}>
        <Text style={styles.icon}>{riskConfig.icon}</Text>
      </View>

      <Text style={styles.label}>{riskConfig.label}</Text>
      <Text style={styles.description}>{riskConfig.description}</Text>

      {showDetails && score !== undefined && (
        <View style={styles.scoreContainer}>
          <Text style={styles.scoreLabel}>Risk Score</Text>
          <View style={{ flexDirection: 'row', alignItems: 'baseline' }}>
            <Text style={styles.scoreValue}>{score}</Text>
            <Text style={styles.scoreUnit}>/100</Text>
          </View>
        </View>
      )}
    </View>
  );
};

/**
 * Mini Risk Indicator
 * Smaller version for dashboard/summary views
 */
export const MiniRiskIndicator = ({ riskLevel, size = 60 }) => {
  const riskConfig = getRiskConfig(riskLevel);

  const styles = StyleSheet.create({
    indicator: {
      width: size,
      height: size,
      borderRadius: BorderRadius.full,
      backgroundColor: riskConfig.color,
      justifyContent: 'center',
      alignItems: 'center',
    },
    icon: {
      fontSize: size * 0.5,
      color: Colors.WHITE,
      fontWeight: 'bold',
    },
  });

  return (
    <View style={styles.indicator}>
      <Text style={styles.icon}>{riskConfig.icon}</Text>
    </View>
  );
};

/**
 * Risk Badge
 * Inline badge for displaying risk level
 */
export const RiskBadge = ({ riskLevel }) => {
  const riskConfig = getRiskConfig(riskLevel);

  const styles = StyleSheet.create({
    badge: {
      backgroundColor: riskConfig.color,
      paddingHorizontal: Spacing.md,
      paddingVertical: Spacing.sm,
      borderRadius: BorderRadius.lg,
      alignItems: 'center',
    },
    text: {
      color: Colors.WHITE,
      fontSize: 14,
      fontWeight: '600',
    },
  });

  return (
    <View style={styles.badge}>
      <Text style={styles.text}>{riskConfig.label}</Text>
    </View>
  );
};

function getRiskConfig(riskLevel) {
  const configs = {
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

  return configs[riskLevel] || configs.HEALTHY;
}
