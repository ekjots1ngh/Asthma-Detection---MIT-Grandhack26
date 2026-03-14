/**
 * Root Navigation Setup
 * Manages screen navigation between Home, Recording, and Results
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Colors } from '../theme';

import HomeScreen from '../screens/HomeScreen';
import RecordingScreen from '../screens/RecordingScreen';
import ResultsScreen from '../screens/ResultsScreen';

const Stack = createNativeStackNavigator();

export const RootNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
          cardStyle: { backgroundColor: Colors.BACKGROUND },
          animationEnabled: true,
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{
            title: 'Breathing Check',
          }}
        />

        <Stack.Screen
          name="Recording"
          component={RecordingScreen}
          options={{
            title: 'Recording',
            cardStyle: { backgroundColor: Colors.BACKGROUND },
          }}
        />

        <Stack.Screen
          name="Results"
          component={ResultsScreen}
          options={{
            title: 'Results',
            cardStyle: { backgroundColor: Colors.BACKGROUND },
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default RootNavigator;
