from Configs import piano_notes_sharps

#piano_notes = ['A0', 'A0#', 'B0', 'C1', 'C1#', 'D1', 'D1#', 'E1', 'F1', 'F1#', 'G1', 'G1#',
              # 'A1', 'A1#', 'B1', 'C2', 'C2#', 'D2', 'D2#', 'E2', 'F2', 'F2#', 'G2', 'G2#',
              # 'A2', 'A2#', 'B2', 'C3', 'C3#', 'D3', 'D3#', 'E3', 'F3', 'F3#', 'G3', 'G3#',
              # 'A3', 'A3#', 'B3', 'C4', 'C4#', 'D4', 'D4#', 'E4', 'F4', 'F4#', 'G4', 'G4#',
              # 'A4', 'A4#', 'B4', 'C5', 'C5#', 'D5', 'D5#', 'E5', 'F5', 'F5#', 'G5', 'G5#',
              # 'A5', 'A5#', 'B5', 'C6', 'C6#', 'D6', 'D6#', 'E6', 'F6', 'F6#', 'G6', 'G6#',
               #'A6', 'A6#', 'B6', 'C7', 'C7#', 'D7', 'D7#', 'E7', 'F7', 'F7#', 'G7', 'G7#',
              # 'A7', 'A7#', 'B7', 'C8']

# C key
#print(len(piano_notes))
#C_pattern = [s for s in piano_notes if "#" not in s]

#print(C_pattern)

#print("----------------------------------------------------------------------------------")
# filter C# pattern
#filtered_indexes = [i for i, s in enumerate(piano_notes) if "#" not in s]

#print(len(filtered_indexes))
#print(filtered_indexes)

# G -> has one # on all Fs

g_pattern = [
    s for s in piano_notes_sharps
    if ("#" not in s and not s.startswith("F")) or (s.startswith("F") and "#" in s)
]
g_pattern_indexes = [
    i for i, s in enumerate(piano_notes_sharps)
    if ("#" not in s and not s.startswith("F")) or (s.startswith("F") and "#" in s)
]

#print(g_pattern)
#print(g_pattern_indexes)
#print(len(g_pattern_indexes))
#print("----------------------------------------------------------------------------------")