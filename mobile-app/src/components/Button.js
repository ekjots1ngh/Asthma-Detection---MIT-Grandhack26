/**
 * Button Component
 * Large, child-friendly button with minimum touch target size
 */

import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
  View,
} from 'react-native';
import { Colors, Spacing, BorderRadius, Typography } from '../theme';

export const LargeButton = ({
  title,
  onPress,
  loading = false,
  disabled = false,
  variant = 'primary',
  size = 'large',
  icon = null,
  testID,
}) => {
  const styles = StyleSheet.create({
    button: {
      height: size === 'large' ? 80 : 60,
      borderRadius: BorderRadius.xl,
      justifyContent: 'center',
      alignItems: 'center',
      paddingHorizontal: Spacing.lg,
      opacity: disabled ? 0.5 : 1,
      ...getVariantStyles(variant),
    },
    container: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
    },
    text: {
      fontSize: size === 'large' ? 24 : 18,
      fontWeight: 'bold',
      marginLeft: icon ? Spacing.md : 0,
      color: variant === 'primary' ? Colors.WHITE : Colors.DARK,
    },
    icon: {
      fontSize: size === 'large' ? 36 : 24,
    },
  });

  return (
    <TouchableOpacity
      style={styles.button}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
      testID={testID}
    >
      {loading ? (
        <ActivityIndicator size="large" color={Colors.WHITE} />
      ) : (
        <View style={styles.container}>
          {icon && <Text style={styles.icon}>{icon}</Text>}
          <Text style={styles.text}>{title}</Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

export const SmallButton = ({
  title,
  onPress,
  variant = 'secondary',
  testID,
}) => {
  const styles = StyleSheet.create({
    button: {
      height: 50,
      borderRadius: BorderRadius.lg,
      justifyContent: 'center',
      alignItems: 'center',
      paddingHorizontal: Spacing.lg,
      ...getVariantStyles(variant),
    },
    text: {
      fontSize: 16,
      fontWeight: '600',
      color: variant === 'primary' ? Colors.WHITE : Colors.DARK,
    },
  });

  return (
    <TouchableOpacity
      style={styles.button}
      onPress={onPress}
      activeOpacity={0.7}
      testID={testID}
    >
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  );
};

function getVariantStyles(variant) {
  const variants = {
    primary: {
      backgroundColor: Colors.INFO,
    },
    success: {
      backgroundColor: Colors.SUCCESS,
    },
    warning: {
      backgroundColor: Colors.WARNING,
    },
    danger: {
      backgroundColor: Colors.ERROR,
    },
    secondary: {
      backgroundColor: Colors.LIGHT_GRAY,
      borderWidth: 2,
      borderColor: Colors.DARK_GRAY,
    },
  };

  return variants[variant] || variants.primary;
}
