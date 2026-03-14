/**
 * Recording Screen
 * Simple instructions and recording interface
 *
 * Shows large visual instructions and animated recording indicator
 * Minimal text for children aged 5-11
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  Animated,
  Dimensions,
} from 'react-native';
import { Audio } from 'expo-av';
import { LargeButton } from '../components/Button';
import { Colors, Spacing, Typography, BorderRadius } from '../theme';

const { width } = Dimensions.get('window');

export const RecordingScreen = ({ navigation }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [permission, setPermission] = useState(null);
  const scaleAnim = new Animated.Value(1);
  const opacityAnim = new Animated.Value(0.6);

  // Request microphone permission
  useEffect(() => {
    requestAudioPermission();
  }, []);

  // Timer for recording duration
  useEffect(() => {
    let interval;
    if (isRecording) {
      interval = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  // Pulsing animation
  useEffect(() => {
    if (isRecording) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(scaleAnim, {
            toValue: 1.1,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(scaleAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      ).start();

      Animated.loop(
        Animated.sequence([
          Animated.timing(opacityAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(opacityAnim, {
            toValue: 0.6,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      ).start();
    }
  }, [isRecording]);

  const requestAudioPermission = async () => {
    try {
      const { status } = await Audio.requestPermissionsAsync();
      setPermission(status === 'granted');
    } catch (err) {
      console.error('Permission error:', err);
    }
  };

  const handleStartRecording = async () => {
    if (!permission) {
      alert('Microphone permission required');
      return;
    }

    try {
      setIsRecording(true);
      setRecordingTime(0);

      // Start recording audio (implementation would go here)
      // This is a placeholder for actual audio recording logic
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    // Simulate analysis and move to results
    setTimeout(() => {
      navigation.navigate('Results', {
        recordingTime,
        riskLevel: 'HEALTHY', // This would be determined by analysis
        score: 85,
      });
    }, 1000);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const styles = StyleSheet.create({
    safeArea: {
      flex: 1,
      backgroundColor: Colors.BACKGROUND,
    },
    container: {
      flex: 1,
      justifyContent: 'space-between',
      paddingHorizontal: Spacing.lg,
      paddingVertical: Spacing.xl,
    },
    headerSection: {
      alignItems: 'center',
    },
    headerTitle: {
      ...Typography.h2,
      color: Colors.DARK,
      marginBottom: Spacing.sm,
    },
    instructionContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    animatedCircle: {
      width: width * 0.5,
      height: width * 0.5,
      borderRadius: (width * 0.5) / 2,
      backgroundColor: Colors.INFO,
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: Spacing.xl,
    },
    recordingIcon: {
      fontSize: 80,
    },
    instructionText: {
      ...Typography.h2,
      color: Colors.DARK,
      marginBottom: Spacing.md,
      textAlign: 'center',
    },
    instructionSmallText: {
      ...Typography.body,
      color: Colors.DARK_GRAY,
      textAlign: 'center',
      marginBottom: Spacing.lg,
      lineHeight: 24,
    },
    stepsContainer: {
      marginVertical: Spacing.xl,
    },
    step: {
      flexDirection: 'row',
      marginBottom: Spacing.lg,
      alignItems: 'flex-start',
    },
    stepNumber: {
      ...Typography.h3,
      color: Colors.INFO,
      marginRight: Spacing.md,
      minWidth: 40,
    },
    stepText: {
      ...Typography.body,
      color: Colors.DARK,
      flex: 1,
      lineHeight: 24,
    },
    timerSection: {
      alignItems: 'center',
      marginVertical: Spacing.lg,
    },
    timerLabel: {
      ...Typography.label,
      color: Colors.GRAY,
      marginBottom: Spacing.sm,
    },
    timerValue: {
      ...Typography.h1,
      color: Colors.INFO,
      fontSize: 48,
    },
    timerDot: {
      width: 12,
      height: 12,
      borderRadius: 6,
      backgroundColor: Colors.INFO,
      marginHorizontal: Spacing.sm,
    },
    buttonSection: {
      gap: Spacing.lg,
    },
  });

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.headerSection}>
          <Text style={styles.headerTitle}>
            {isRecording ? 'Recording...' : 'Get Ready'}
          </Text>
        </View>

        {/* Main Content */}
        <View style={styles.instructionContainer}>
          {isRecording ? (
            <>
              {/* Recording State */}
              <Animated.View
                style={[
                  styles.animatedCircle,
                  {
                    transform: [{ scale: scaleAnim }],
                    opacity: opacityAnim,
                  },
                ]}
              >
                <Text style={styles.recordingIcon}>🎤</Text>
              </Animated.View>

              <Text style={styles.instructionText}>Keep listening</Text>
              <Text style={styles.instructionSmallText}>
                Stay still and keep the phone close to your mouth
              </Text>

              {/* Timer */}
              <View style={styles.timerSection}>
                <Text style={styles.timerLabel}>Recording Time</Text>
                <Text style={styles.timerValue}>{formatTime(recordingTime)}</Text>
              </View>
            </>
          ) : (
            <>
              {/* Pre-Recording Instructions */}
              <Text style={styles.instructionText}>How to Check</Text>

              <View style={styles.stepsContainer}>
                <View style={styles.step}>
                  <Text style={styles.stepNumber}>1</Text>
                  <Text style={styles.stepText}>Find a quiet place</Text>
                </View>

                <View style={styles.step}>
                  <Text style={styles.stepNumber}>2</Text>
                  <Text style={styles.stepText}>
                    Hold phone close to your mouth
                  </Text>
                </View>

                <View style={styles.step}>
                  <Text style={styles.stepNumber}>3</Text>
                  <Text style={styles.stepText}>Breathe normally for 15 seconds</Text>
                </View>

                <View style={styles.step}>
                  <Text style={styles.stepNumber}>4</Text>
                  <Text style={styles.stepText}>We'll analyze the results</Text>
                </View>
              </View>

              <Text style={styles.instructionSmallText}>
                📱 Make sure it's quiet so we can hear clearly
              </Text>
            </>
          )}
        </View>

        {/* Buttons */}
        <View style={styles.buttonSection}>
          {!isRecording ? (
            <LargeButton
              title="Start Check"
              onPress={handleStartRecording}
              variant="primary"
              icon="▶"
            />
          ) : (
            <LargeButton
              title="Stop"
              onPress={handleStopRecording}
              variant="danger"
              icon="⏹"
            />
          )}
        </View>
      </View>
    </SafeAreaView>
  );
};

export default RecordingScreen;
