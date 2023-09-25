import { extendTheme, theme } from "@chakra-ui/react";

export const appTheme = extendTheme({
  colors: {
    brand: {
      primary: "#001EA7",
      secondary: "#2351DC",
    },

    content: {
      primary: "#00001F",
      secondary: "#00001F",
      tertiary: "#7A7B9A",
      link: "#2351DC",
      alternative: "#001EA7",
    },

    semantic: {
      success: "#24BE00",
      successOverlay: "#EFFDE5",
      warning: "#C98300",
      warningOverlay: "#FEF8E1",
      danger: "#F23D33",
      dangerOverlay: "#FFEAEE",
    },

    base: {
      light: "#FFFFFF",
      dark: "#00001F",
    },

    border: {
      neutral: "#D7D8FA",
      overlay: "#E6E7FF",
    },

    background: {
      default: "#FFFFFF",
      neutral: "#E8EAFB",
      alternative: "#EFFDE5",
      overlay: "#C5CBF5",
      transparentGrey: "rgba(232, 234, 251, 0.20)",
    },

    interactive: {
      primary: "#008600",
      primaryLight: "#61c261",
      accent: "#5FE500",
      secondary: "#2351DC",
      tertiary: "#24BE00",
      quaternary: "#F17105",
      control: "#7A7B9A",
      connected: "#FA7200",
    },

    sentiment: {
      positiveOverlay: "#EFFDE5",
      positiveLight: "#f0f7eb",
      positiveDark: "#b9cfa9",
      positiveDefault: "#24BE00",
      warningDefault: "#C98300",
      warningOverlay: "#FEF8E1",
      negativeDefault: "#F23D33",
    },

    brandScheme: {
      100: "#C5CBF5",
      500: "#2351DC",
    },

    body: "#232640",
  },

  fonts: {
    heading: "var(--font-poppins)",
    body: "var(--font-opensans)",
  },

  fontSizes: {
    display: {
      lg: "57px",
      md: "45px",
      sm: "36px",
    },

    headline: {
      lg: "32px",
      md: "36px",
      sm: "24px",
    },

    title: {
      lg: "22px",
      md: "16px",
      sm: "14px",
    },

    label: {
      lg: "14px",
      md: "12px",
      sm: "11px",
    },

    body: {
      xl: "22px",
      lg: "16px",
      md: "14px",
      sm: "12px",
    },

    button: {
      lg: "20px",
      md: "14px",
      sm: "12px",
    },

    caption: "12px",
    overline: "10px",
  },

  fontWeights: {
    hairline: 100,
    thin: 200,
    light: 300,
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },

  lineHeights: {
    normal: "normal",
    none: 1,
    "64": "64px",
    "52": "52px",
    "44": "44px",
    "40": "40px",
    "36": "36px",
    "32": "32px",
    "28": "28px",
    "24": "24px",
    "20": "20px",
    "16": "16px",
  },

  letterSpacing: {
    normal: 0,
    wide: "0.5px",
    wider: "1.25px",
    widest: "1.5px",
  },

  spacing: {
    xs: "4px",
    s: "8px",
    m: "16px",
    l: "24px",
    xl: "32px",
    xxl: "40px",
    "xxl-2": "48px",
    "xxl-3": "56px",
    "xxl-4": "64px",
    "xxl-5": "72px",
    "xxl-6": "80px",
  },

  shadows: {
    "1dp": "0px 1px 2px -1px #0000001A, 0px 1px 3px 0px #00001F1A",
    "2dp": "0px 2px 4px -2px #0000001A, 0px 4px 6px -1px #0000001A",
    "4dp": "0px 4px 6px -4px #0000001A, 0px 10px 15px -3px #0000001A",
    "8dp": "0px 8px 10px -6px #0000001A, 0px 20px 25px -5px #0000001A",
    "12dp": "0px 25px 50px -12px #00000040",
  },

  borderRadius: {
    full: "50%",
    minimal: "4px",
    rounded: "8px",
    "rounded-xl": "16px",
    "rounded-xxl": "20px",
  },

  breakpoints: {
    xs: "360px",
    sm: "600px",
    md: "905px",
    lg: "1240px",
    xl: "1440px",
  },

  components: {
    Button: {
      baseStyle: {
        textTransform: "uppercase",
        borderRadius: 50,
      },
      variants: {
        outline: {
          border: "2px solid",
          borderColor: "#2351DC",
          color: "#2351DC",
          _hover: {
            transform: "scale(0.98)",
            borderColor: "#5a7be0",
            color: "#5a7be0",
          },
          _active: {
            borderColor: "#899ee0",
            color: "#899ee0",
          },
          _loading: {
            opacity: 0.8,
          },
        },
        solid: {
          bg: "#2351DC",
          color: "white",
          _hover: {
            transform: "scale(0.98)",
            bg: "#5a7be0",
          },
          _active: {
            bg: "#899ee0",
          },
          _loading: {
            opacity: 0.8,
            _hover: {
              bg: "#5a7be0",
            },
          },
        },
        solidPrimary: {
          ...theme.components.Button.variants?.solid,
          bg: "sentiment.positiveOverlay",
          color: "interactive.primary",
          _hover: {
            transform: "scale(0.98)",
            bg: "sentiment.positiveLight",
            color: "interactive.primaryLight",
          },
          _active: {
            bg: "sentiment.positiveDark",
            color: "sentiment.positiveOverlay",
          },
          _loading: {
            opacity: 0.8,
            bg: "sentiment.positiveLight",
          },
        },
        ghost: {
          color: "#5a7be0",
        },
        solidIcon: {
          bgColor: "background.neutral",
          color: "interactive.secondary",
          _hover: {
            color: "white",
            bg: "#5a7be0",
          },
          _active: {
            bg: "#899ee0",
          },
        },
      },
    },
    Link: {
      baseStyle: {
        color: "brand.secondary",
      },
    },
    Card: {
      baseStyle: {
        container: {
          borderRadius: 8,
          px: 6,
          py: 8,
        },
      },
    },
    Tag: {
      variants: {
        brand: {
          container: {
            px: 3,
            py: 1,
            borderRadius: "full",
            borderColor: "background.neutral",
            borderWidth: 1,
            color: "background.neutral",
          },
          label: {
            color: "content.secondary",
            fontSize: "14",
            borderWidth: 0,
            mt: -0.5,
          },
        },
        filled: {
          container: {
            px: 4,
            py: 1,
            borderRadius: "full",
            bgColor: "background.neutral",
          },
          label: {
            color: "content.alternative",
          },
        },
        success: {
          container: {
            px: 4,
            py: 1,
            borderRadius: "full",
            borderWidth: 1,
            borderColor: "sentiment.positiveDefault",
            bgColor: "sentiment.positiveOverlay",
            color: "sentiment.positiveDefault",
            fontWeight: 500,
          },
          label: {
            color: "sentiment.positiveDefault",
          },
        },
        warning: {
          container: {
            px: 4,
            py: 1,
            borderRadius: "full",
            borderWidth: 1,
            borderColor: "sentiment.warningDefault",
            bgColor: "sentiment.warningOverlay",
            color: "sentiment.warningDefault",
          },
          label: {
            color: "sentiment.warningDefault",
          },
        },
      },
      defaultProps: {
        variant: "brand",
      },
    },
    Tooltip: {
      baseStyle: {
        bg: "content.secondary",
        color: "base.light",
        px: 4,
        py: 2,
        borderRadius: "lg",
      },
    },
    Tabs: {
      variants: {
        line: {
          tab: {
            _selected: {
              color: "interactive.secondary",
              borderColor: "interactive.secondary",
              fontWeight: "bold",
            },
          },
        },
      },
    },
    Accordion: {
      variants: {
        brand: {
          container: {
            borderRadius: "8px",
            bgColor: "background.transparentGrey",
            borderWidth: 0,
            px: 4,
            py: 4,
            mb: 6,
          },
          button: {
            borderRadius: "8px",
          },
        },
      },
      defaultProps: {
        variant: "brand",
      },
    },
  },
});