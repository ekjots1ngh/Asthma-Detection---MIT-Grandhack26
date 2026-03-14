/**
 * Breathing Check App
 * Main entry point for the asthma symptom monitoring app
 *
 * Simple, child-friendly interface for monitoring respiratory health
 */

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { RootNavigator } from './src/navigation/RootNavigator';
import { Colors } from './src/theme';

export default function App() {
  return (
    <>
      <RootNavigator />
      <StatusBar barStyle="dark-content" backgroundColor={Colors.BACKGROUND} />
    </>
  );
}
