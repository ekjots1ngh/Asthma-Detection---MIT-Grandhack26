/**
 * Results Screen
 * Display color-coded results with risk indicator
 *
 * Green/Yellow/Red indicator system for quick assessment
 * Actionable guidance for parents
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Dimensions,
} from 'react-native';
import { RiskIndicator } from '../components/RiskIndicator';
import { LargeButton, SmallButton } from '../components/Button';
import { Colors, Spacing, Typography, BorderRadius } from '../theme';

const { width } = Dimensions.get('window');

export const ResultsScreen = ({ route, navigation }) => {
  const { riskLevel = 'HEALTHY', score = 85, metrics = {} } = route.params || {};

  const getGuidance = (level) => {
    const guidance = {
      HEALTHY: {
        title: 'All Good!',
        message: 'Your child\'s breathing is healthy.',
        actions: ['Continue regular check-ups', 'Follow medication as prescribed'],
        color: Colors.GREEN,
      },
      WARNING: {
        title: 'Monitor Closely',
        message: 'Watch for changes in breathing. No immediate action needed.',
        actions: [
          'Keep medication nearby',
          'Monitor for other symptoms',
          'Schedule a check-up if it persists',
        ],
        color: Colors.YELLOW,
      },
      CRITICAL: {
        title: 'Take Action',
        message: 'Please contact your healthcare provider today.',
        actions: [
          'Call your doctor',
          'Use rescue inhaler if prescribed',
          'Go to urgent care if breathing worsens',
        ],
        color: Colors.RED,
      },
    };
    return guidance[level] || guidance.HEALTHY;
  };

  const guidance = getGuidance(riskLevel);

  const styles = StyleSheet.create({
    safeArea: {
      flex: 1,
      backgroundColor: Colors.BACKGROUND,
    },
    container: {
      flex: 1,
    },
    scrollContent: {
      padding: Spacing.lg,
      paddingBottom: Spacing.xl,
    },
    headerSection: {
      alignItems: 'center',
      marginBottom: Spacing.xl,
    },
    headerText: {
      ...Typography.h2,
      color: Colors.DARK,
      marginBottom: Spacing.md,
    },
    riskIndicatorSection: {
      alignItems: 'center',
      marginVertical: Spacing.xl,
    },
    metricsSection: {
      backgroundColor: Colors.SURFACE,
      borderRadius: BorderRadius.lg,
      padding: Spacing.lg,
      marginVertical: Spacing.lg,
    },
    metricsTitle: {
      ...Typography.h3,
      color: Colors.DARK,
      marginBottom: Spacing.md,
    },
    metricRow: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      paddingVertical: Spacing.md,
      borderBottomWidth: 1,
      borderBottomColor: Colors.LIGHT_GRAY,
    },
    metricLabel: {
      ...Typography.body,
      color: Colors.DARK_GRAY,
    },
    metricValue: {
      ...Typography.body,
      fontWeight: '600',
      color: Colors.DARK,
    },
    guidanceSection: {
      backgroundColor: guidance.color,
      borderRadius: BorderRadius.lg,
      padding: Spacing.lg,
      marginVertical: Spacing.lg,
    },
    guidanceTitle: {
      ...Typography.h3,
      color: Colors.WHITE,
      marginBottom: Spacing.md,
    },
    guidanceMessage: {
      ...Typography.body,
      color: Colors.WHITE,
      lineHeight: 24,
      marginBottom: Spacing.lg,
    },
    actionsList: {
      backgroundColor: 'rgba(255, 255, 255, 0.2)',
      borderRadius: BorderRadius.md,
      padding: Spacing.md,
    },
    actionItem: {
      flexDirection: 'row',
      marginVertical: Spacing.sm,
      alignItems: 'flex-start',
    },
    actionBullet: {
      ...Typography.body,
      color: Colors.WHITE,
      marginRight: Spacing.sm,
      marginTop: 2,
    },
    actionText: {
      ...Typography.body,
      color: Colors.WHITE,
      flex: 1,
      lineHeight: 22,
    },
    disclaimerSection: {
      backgroundColor: Colors.LIGHT_GRAY,
      borderRadius: BorderRadius.lg,
      padding: Spacing.lg,
      marginVertical: Spacing.lg,
    },
    disclaimerText: {
      ...Typography.small,
      color: Colors.DARK_GRAY,
      lineHeight: 20,
    },
    buttonSection: {
      gap: Spacing.lg,
    },
    divider: {
      height: 1,
      backgroundColor: Colors.LIGHT_GRAY,
      marginVertical: Spacing.lg,
    },
  });

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.headerSection}>
          <Text style={styles.headerText}>Your Results</Text>
        </View>

        {/* Risk Indicator */}
        <View style={styles.riskIndicatorSection}>
          <RiskIndicator
            riskLevel={riskLevel}
            score={score}
            showDetails={true}
          />
        </View>

        {/* Metrics */}
        {Object.keys(metrics).length > 0 && (
          <View style={styles.metricsSection}>
            <Text style={styles.metricsTitle}>Details</Text>

            {metrics.coughCount !== undefined && (
              <View style={styles.metricRow}>
                <Text style={styles.metricLabel}>Coughs Detected</Text>
                <Text style={styles.metricValue}>{metrics.coughCount}</Text>
              </View>
            )}

            {metrics.respiratoryRate !== undefined && (
              <View style={styles.metricRow}>
                <Text style={styles.metricLabel}>Breathing Rate</Text>
                <Text style={styles.metricValue}>
                  {metrics.respiratoryRate} breaths/min
                </Text>
              </View>
            )}

            {metrics.wheezeDetected !== undefined && (
              <View style={styles.metricRow}>
                <Text style={styles.metricLabel}>Wheeze Sound</Text>
                <Text style={styles.metricValue}>
                  {metrics.wheezeDetected ? 'Detected' : 'Not detected'}
                </Text>
              </View>
            )}

            {metrics.recordingDuration !== undefined && (
              <View style={[styles.metricRow, { borderBottomWidth: 0 }]}>
                <Text style={styles.metricLabel}>Recording Duration</Text>
                <Text style={styles.metricValue}>
                  {metrics.recordingDuration}s
                </Text>
              </View>
            )}
          </View>
        )}

        {/* Guidance */}
        <View style={styles.guidanceSection}>
          <Text style={styles.guidanceTitle}>{guidance.title}</Text>
          <Text style={styles.guidanceMessage}>{guidance.message}</Text>

          <View style={styles.actionsList}>
            {guidance.actions.map((action, index) => (
              <View key={index} style={styles.actionItem}>
                <Text style={styles.actionBullet}>•</Text>
                <Text style={styles.actionText}>{action}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Disclaimer */}
        <View style={styles.disclaimerSection}>
          <Text style={styles.disclaimerText}>
            ⓘ This app provides general guidance only. Always consult with your
            healthcare provider for medical advice, diagnosis, or treatment. In
            case of emergency, call 911.
          </Text>
        </View>

        {/* Buttons */}
        <View style={styles.buttonSection}>
          <LargeButton
            title="Check Again"
            onPress={() => navigation.navigate('Recording')}
            variant="primary"
          />

          <SmallButton
            title="Back to Home"
            onPress={() => navigation.navigate('Home')}
            variant="secondary"
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default ResultsScreen;
