/**
 * Home Screen
 * Main entry point with large "Check Breathing" button
 *
 * Simple, minimal design suitable for children aged 5-11
 * Parents can quickly check child's breathing status
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Image,
} from 'react-native';
import { LargeButton, SmallButton } from '../components/Button';
import { MiniRiskIndicator } from '../components/RiskIndicator';
import { Colors, Spacing, Typography, BorderRadius } from '../theme';

export const HomeScreen = ({ navigation }) => {
  const [lastCheckTime, setLastCheckTime] = useState(null);
  const [lastRiskLevel, setLastRiskLevel] = useState('HEALTHY');

  const handleStartCheck = () => {
    // Navigate to recording screen
    navigation.navigate('Recording');
  };

  const handleViewHistory = () => {
    // Navigate to history/results screen
    navigation.navigate('Results');
  };

  const formatTimeAgo = (timestamp) => {
    if (!timestamp) return null;
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  };

  const styles = StyleSheet.create({
    safeArea: {
      flex: 1,
      backgroundColor: Colors.BACKGROUND,
    },
    container: {
      flex: 1,
      paddingHorizontal: Spacing.lg,
      paddingTop: Spacing.xl,
    },
    scrollContent: {
      flexGrow: 1,
      justifyContent: 'space-between',
      paddingBottom: Spacing.xl,
    },
    headerSection: {
      alignItems: 'center',
      marginBottom: Spacing.xl,
    },
    logo: {
      width: 80,
      height: 80,
      marginBottom: Spacing.lg,
    },
    title: {
      ...Typography.h1,
      fontSize: 36,
      color: Colors.DARK,
      marginBottom: Spacing.sm,
      textAlign: 'center',
    },
    subtitle: {
      ...Typography.body,
      color: Colors.DARK_GRAY,
      textAlign: 'center',
      marginBottom: Spacing.lg,
    },
    buttonSection: {
      marginBottom: Spacing.xl,
    },
    mainButton: {
      marginBottom: Spacing.lg,
    },
    lastCheckSection: {
      backgroundColor: Colors.SURFACE,
      borderRadius: BorderRadius.lg,
      padding: Spacing.lg,
      marginBottom: Spacing.xl,
    },
    lastCheckLabel: {
      ...Typography.label,
      color: Colors.GRAY,
      marginBottom: Spacing.sm,
    },
    lastCheckContent: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
    },
    lastCheckText: {
      ...Typography.body,
      color: Colors.DARK,
      flex: 1,
    },
    lastCheckTime: {
      ...Typography.small,
      color: Colors.GRAY,
      marginTop: Spacing.xs,
    },
    statusContainer: {
      flexDirection: 'column',
      alignItems: 'center',
    },
    statusIcon: {
      marginBottom: Spacing.sm,
    },
    quickActionSection: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      marginTop: Spacing.lg,
      paddingTop: Spacing.lg,
      borderTopWidth: 1,
      borderTopColor: Colors.LIGHT_GRAY,
    },
    actionButton: {
      flex: 1,
      marginHorizontal: Spacing.sm,
    },
    tipSection: {
      backgroundColor: Colors.INFO,
      borderRadius: BorderRadius.lg,
      padding: Spacing.lg,
      marginTop: Spacing.lg,
    },
    tipLabel: {
      ...Typography.label,
      color: Colors.WHITE,
      marginBottom: Spacing.sm,
    },
    tipText: {
      ...Typography.body,
      color: Colors.WHITE,
      lineHeight: 24,
    },
  });

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
      >
        {/* Header */}
        <View style={styles.headerSection}>
          <Text style={styles.title}>Breathing</Text>
          <Text style={styles.title}>Check</Text>
          <Text style={styles.subtitle}>Monitor your child's breathing</Text>
        </View>

        {/* Last Check Status */}
        {lastCheckTime && (
          <View style={styles.lastCheckSection}>
            <Text style={styles.lastCheckLabel}>LAST CHECK</Text>
            <View style={styles.lastCheckContent}>
              <View style={{ flex: 1 }}>
                <Text style={styles.lastCheckText}>Status</Text>
                <Text style={styles.lastCheckTime}>
                  {formatTimeAgo(lastCheckTime)}
                </Text>
              </View>
              <View style={styles.statusContainer}>
                <View style={styles.statusIcon}>
                  <MiniRiskIndicator riskLevel={lastRiskLevel} size={48} />
                </View>
              </View>
            </View>
          </View>
        )}

        {/* Main Button */}
        <View style={styles.buttonSection}>
          <View style={styles.mainButton}>
            <LargeButton
              title="Check Breathing"
              onPress={handleStartCheck}
              variant="primary"
              icon="🎤"
            />
          </View>

          {/* Tip */}
          <View style={styles.tipSection}>
            <Text style={styles.tipLabel}>💡 Tip</Text>
            <Text style={styles.tipText}>
              Make sure it's quiet so we can hear breathing clearly
            </Text>
          </View>
        </View>

        {/* Quick Actions */}
        <View style={styles.quickActionSection}>
          <View style={styles.actionButton}>
            <SmallButton
              title="History"
              onPress={handleViewHistory}
              variant="secondary"
            />
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default HomeScreen;
