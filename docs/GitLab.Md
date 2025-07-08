## Control when jobs run:    only / except (deprecated, use rules)  
```
only:
  - main
except:
  - tags
  ``` 

## rules (recommended):  
```
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
    when: always
  - if: '$CI_COMMIT_BRANCH =~ /feature-*/'
    when: manual
```  
