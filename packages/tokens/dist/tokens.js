// 이 파일은 tokens.css에서 생성된다. 직접 수정하지 않는다.
export const tokens = {
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$description": "kor-travel-common의 --kt-* 디자인 토큰. 값의 정본은 tokens.css이다.",
  "color": {},
  "dimension": {},
  "duration": {
    "fast": {
      "$type": "duration",
      "$value": "100ms",
      "$extensions": {
        "kor-travel-common": {
          "dark": "100ms"
        }
      }
    },
    "base": {
      "$type": "duration",
      "$value": "150ms",
      "$extensions": {
        "kor-travel-common": {
          "dark": "150ms"
        }
      }
    }
  },
  "cubicBezier": {},
  "shadow": {
    "elevated": {
      "$type": "shadow",
      "$value": "0 4px 12px oklch(30% 0.006 157 / 0.1)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "0 4px 12px oklch(10% 0.006 157 / 0.32)"
        }
      }
    },
    "modal": {
      "$type": "shadow",
      "$value": "0 8px 24px oklch(30% 0.006 157 / 0.14)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "0 8px 24px oklch(10% 0.006 157 / 0.4)"
        }
      }
    }
  },
  "number": {},
  "fontFamily": {},
  "profiles": {
    "admin": {
      "$description": "공용 admin 밀도 프로필",
      "radius": {
        "control": "0.375rem",
        "panel": "0.5rem"
      },
      "controlHeight": {
        "default": "2.25rem",
        "small": "1.875rem"
      },
      "body": "0.9375rem",
      "typeScale": [
        "0.75rem",
        "0.84375rem",
        "0.9375rem",
        "1.0625rem",
        "1.25rem",
        "1.5rem",
        "1.875rem"
      ]
    },
    "consumer": {
      "$description": "의미 이름만 common이 제공하며 값과 밀도는 소비자가 소유한다.",
      "ownedBy": "consumer",
      "semanticGroups": [
        "surface",
        "text",
        "brand",
        "status",
        "font"
      ]
    }
  },
  "surface": {
    "page": {
      "$type": "color",
      "$value": "oklch(97.8% 0.003 128)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(19% 0.006 150)"
        }
      }
    },
    "subtle": {
      "$type": "color",
      "$value": "oklch(96.7% 0.006 138)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(24% 0.008 145)"
        }
      }
    },
    "muted": {
      "$type": "color",
      "$value": "oklch(92.5% 0.01 141)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(31% 0.012 145)"
        }
      }
    },
    "card": {
      "$type": "color",
      "$value": "oklch(99.2% 0.002 140)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(23% 0.007 145)"
        }
      }
    }
  },
  "text": {
    "primary": {
      "$type": "color",
      "$value": "oklch(30% 0.006 157)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(93% 0.006 155)"
        }
      }
    },
    "secondary": {
      "$type": "color",
      "$value": "oklch(48% 0.012 159)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(78% 0.01 155)"
        }
      }
    },
    "tertiary": {
      "$type": "color",
      "$value": "oklch(54% 0.012 154)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(68% 0.012 155)"
        }
      }
    },
    "disabled": {
      "$type": "color",
      "$value": "oklch(79% 0.012 154)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(52% 0.012 155)"
        }
      }
    },
    "strong": {
      "$type": "color",
      "$value": "var(--kt-text-primary)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "var(--kt-text-primary)"
        }
      }
    }
  },
  "icon": {
    "$type": "color",
    "$value": "var(--kt-text-tertiary)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(70% 0.01 155)"
      }
    }
  },
  "border": {
    "$type": "color",
    "$value": "var(--kt-surface-muted)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "var(--kt-surface-muted)"
      }
    }
  },
  "control": {
    "line": {
      "$type": "color",
      "$value": "oklch(61% 0.012 145)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(58% 0.012 145)"
        }
      }
    },
    "h": {
      "$type": "dimension",
      "$value": "2.25rem",
      "$extensions": {
        "kor-travel-common": {
          "dark": "2.25rem"
        }
      }
    },
    "h-sm": {
      "$type": "dimension",
      "$value": "1.875rem",
      "$extensions": {
        "kor-travel-common": {
          "dark": "1.875rem"
        }
      }
    }
  },
  "brand": {
    "$type": "color",
    "$value": "oklch(51.4% 0.081 169)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(76% 0.085 169)"
      }
    },
    "hover": {
      "$type": "color",
      "$value": "oklch(46% 0.085 169)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(81% 0.085 169)"
        }
      }
    },
    "tint": {
      "$type": "color",
      "$value": "oklch(95.2% 0.013 172)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(31% 0.035 169)"
        }
      }
    },
    "foreground": {
      "$type": "color",
      "$value": "oklch(99% 0.002 140)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(20% 0.02 165)"
        }
      }
    }
  },
  "focus": {
    "$type": "color",
    "$value": "oklch(45% 0.09 169)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(80% 0.09 169)"
      }
    }
  },
  "success": {
    "$type": "color",
    "$value": "oklch(46.9% 0.087 149)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(75% 0.09 149)"
      }
    },
    "tint": {
      "$type": "color",
      "$value": "oklch(95% 0.03 150)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(28% 0.04 150)"
        }
      }
    }
  },
  "warning": {
    "$type": "color",
    "$value": "oklch(50.9% 0.103 71)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(77% 0.12 75)"
      }
    },
    "tint": {
      "$type": "color",
      "$value": "oklch(96% 0.035 80)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(30% 0.045 80)"
        }
      }
    }
  },
  "info": {
    "$type": "color",
    "$value": "oklch(50% 0.16 258)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(75% 0.11 258)"
      }
    },
    "tint": {
      "$type": "color",
      "$value": "oklch(95.5% 0.025 255)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(30% 0.05 258)"
        }
      }
    }
  },
  "destructive": {
    "$type": "color",
    "$value": "oklch(51.4% 0.167 27)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(72% 0.14 27)"
      }
    },
    "tint": {
      "$type": "color",
      "$value": "oklch(96% 0.03 25)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "oklch(30% 0.06 27)"
        }
      }
    }
  },
  "overlay": {
    "$type": "color",
    "$value": "oklch(30% 0.006 157 / 0.45)",
    "$extensions": {
      "kor-travel-common": {
        "dark": "oklch(10% 0.006 157 / 0.6)"
      }
    }
  },
  "radius": {
    "control": {
      "$type": "dimension",
      "$value": "0.375rem",
      "$extensions": {
        "kor-travel-common": {
          "dark": "0.375rem"
        }
      }
    },
    "panel": {
      "$type": "dimension",
      "$value": "0.5rem",
      "$extensions": {
        "kor-travel-common": {
          "dark": "0.5rem"
        }
      }
    }
  },
  "rail": {
    "$type": "dimension",
    "$value": "22rem",
    "$extensions": {
      "kor-travel-common": {
        "dark": "22rem"
      }
    }
  },
  "ease": {
    "out": {
      "$type": "cubicBezier",
      "$value": "cubic-bezier(0.16, 1, 0.3, 1)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "cubic-bezier(0.16, 1, 0.3, 1)"
        }
      }
    },
    "in": {
      "$type": "cubicBezier",
      "$value": "cubic-bezier(0.7, 0, 0.84, 0)",
      "$extensions": {
        "kor-travel-common": {
          "dark": "cubic-bezier(0.7, 0, 0.84, 0)"
        }
      }
    }
  },
  "z": {
    "nav": {
      "$type": "number",
      "$value": "30",
      "$extensions": {
        "kor-travel-common": {
          "dark": "30"
        }
      }
    },
    "panel": {
      "$type": "number",
      "$value": "40",
      "$extensions": {
        "kor-travel-common": {
          "dark": "40"
        }
      }
    },
    "overlay": {
      "$type": "number",
      "$value": "50",
      "$extensions": {
        "kor-travel-common": {
          "dark": "50"
        }
      }
    },
    "modal": {
      "$type": "number",
      "$value": "60",
      "$extensions": {
        "kor-travel-common": {
          "dark": "60"
        }
      }
    },
    "toast": {
      "$type": "number",
      "$value": "70",
      "$extensions": {
        "kor-travel-common": {
          "dark": "70"
        }
      }
    }
  },
  "font": {
    "sans": {
      "$type": "fontFamily",
      "$value": "\"Pretendard Variable\", Pretendard, \"Noto Sans KR\", \"Apple SD Gothic Neo\", system-ui, sans-serif",
      "$extensions": {
        "kor-travel-common": {
          "dark": "\"Pretendard Variable\", Pretendard, \"Noto Sans KR\", \"Apple SD Gothic Neo\", system-ui, sans-serif"
        }
      }
    },
    "mono": {
      "$type": "fontFamily",
      "$value": "ui-monospace, \"SF Mono\", Menlo, Consolas, monospace",
      "$extensions": {
        "kor-travel-common": {
          "dark": "ui-monospace, \"SF Mono\", Menlo, Consolas, monospace"
        }
      }
    }
  }
};
export const tokenValues = {
  "--kt-surface-page": "oklch(97.8% 0.003 128)",
  "--kt-surface-subtle": "oklch(96.7% 0.006 138)",
  "--kt-surface-muted": "oklch(92.5% 0.01 141)",
  "--kt-surface-card": "oklch(99.2% 0.002 140)",
  "--kt-text-primary": "oklch(30% 0.006 157)",
  "--kt-text-secondary": "oklch(48% 0.012 159)",
  "--kt-text-tertiary": "oklch(54% 0.012 154)",
  "--kt-text-disabled": "oklch(79% 0.012 154)",
  "--kt-text-strong": "var(--kt-text-primary)",
  "--kt-icon": "var(--kt-text-tertiary)",
  "--kt-border": "var(--kt-surface-muted)",
  "--kt-control-line": "oklch(61% 0.012 145)",
  "--kt-brand": "oklch(51.4% 0.081 169)",
  "--kt-brand-hover": "oklch(46% 0.085 169)",
  "--kt-brand-tint": "oklch(95.2% 0.013 172)",
  "--kt-brand-foreground": "oklch(99% 0.002 140)",
  "--kt-focus": "oklch(45% 0.09 169)",
  "--kt-success": "oklch(46.9% 0.087 149)",
  "--kt-success-tint": "oklch(95% 0.03 150)",
  "--kt-warning": "oklch(50.9% 0.103 71)",
  "--kt-warning-tint": "oklch(96% 0.035 80)",
  "--kt-info": "oklch(50% 0.16 258)",
  "--kt-info-tint": "oklch(95.5% 0.025 255)",
  "--kt-destructive": "oklch(51.4% 0.167 27)",
  "--kt-destructive-tint": "oklch(96% 0.03 25)",
  "--kt-overlay": "oklch(30% 0.006 157 / 0.45)",
  "--kt-radius-control": "0.375rem",
  "--kt-radius-panel": "0.5rem",
  "--kt-control-h": "2.25rem",
  "--kt-control-h-sm": "1.875rem",
  "--kt-rail": "22rem",
  "--kt-duration-fast": "100ms",
  "--kt-duration-base": "150ms",
  "--kt-ease-out": "cubic-bezier(0.16, 1, 0.3, 1)",
  "--kt-ease-in": "cubic-bezier(0.7, 0, 0.84, 0)",
  "--kt-shadow-elevated": "0 4px 12px oklch(30% 0.006 157 / 0.1)",
  "--kt-shadow-modal": "0 8px 24px oklch(30% 0.006 157 / 0.14)",
  "--kt-z-nav": "30",
  "--kt-z-panel": "40",
  "--kt-z-overlay": "50",
  "--kt-z-modal": "60",
  "--kt-z-toast": "70",
  "--kt-font-sans": "\"Pretendard Variable\", Pretendard, \"Noto Sans KR\", \"Apple SD Gothic Neo\", system-ui, sans-serif",
  "--kt-font-mono": "ui-monospace, \"SF Mono\", Menlo, Consolas, monospace"
};
