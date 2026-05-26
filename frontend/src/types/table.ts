export interface ColumnConfig {
  field: string;
  header: string;
  align?: "left" | "right" | "center";
  sortable?: boolean;
}
