#!/usr/bin/env python3
"""
Deduplication script for research papers across multiple papertable files.
Combines all filtered papers and removes duplicates based on DOI, title, and author matching.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple
from difflib import SequenceMatcher
import re

def normalize_string(s: str) -> str:
    """Normalize string for comparison by removing special chars and lowercasing."""
    if not s:
        return ""
    # Remove special characters, extra spaces, convert to lowercase
    s = re.sub(r'[^\w\s]', ' ', s.lower())
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def normalize_authors(authors: List[Dict]) -> str:
    """Create normalized author string for comparison."""
    if not authors:
        return ""
    # Extract author names and sort them
    author_names = []
    for author in authors:
        if isinstance(author, dict):
            name = author.get('name', '')
        else:
            name = str(author)
        if name:
            author_names.append(normalize_string(name))
    return '|'.join(sorted(author_names))

def title_similarity(title1: str, title2: str) -> float:
    """Calculate similarity between two titles."""
    t1 = normalize_string(title1)
    t2 = normalize_string(title2)
    if not t1 or not t2:
        return 0.0
    return SequenceMatcher(None, t1, t2).ratio()

def are_duplicates(paper1: Dict, paper2: Dict, similarity_threshold: float = 0.85) -> bool:
    """
    Determine if two papers are duplicates based on:
    1. Exact DOI match
    2. High title similarity + author overlap
    """
    # Check DOI match (most reliable)
    doi1 = paper1.get('doi', '').strip().lower() if paper1.get('doi') else ''
    doi2 = paper2.get('doi', '').strip().lower() if paper2.get('doi') else ''
    
    if doi1 and doi2 and doi1 == doi2:
        return True
    
    # Check title similarity
    title1 = paper1.get('title', '')
    title2 = paper2.get('title', '')
    
    if not title1 or not title2:
        return False
    
    sim = title_similarity(title1, title2)
    
    # If titles are very similar, check authors
    if sim >= similarity_threshold:
        authors1 = normalize_authors(paper1.get('authors', []))
        authors2 = normalize_authors(paper2.get('authors', []))
        
        # If both have authors, they should have some overlap
        if authors1 and authors2:
            # Check if there's significant author overlap
            auth1_set = set(authors1.split('|'))
            auth2_set = set(authors2.split('|'))
            
            if auth1_set and auth2_set:
                overlap = len(auth1_set & auth2_set)
                min_authors = min(len(auth1_set), len(auth2_set))
                
                # If at least 50% of authors match, consider it a duplicate
                if overlap / min_authors >= 0.5:
                    return True
        else:
            # If no author info available, rely on high title similarity
            if sim >= 0.95:
                return True
    
    return False

def find_papers_column(columns: List) -> str:
    """Find the column ID that contains paper data."""
    for col in columns:
        if isinstance(col, dict):
            col_name = col.get('name', '').lower()
            if 'paper' in col_name:
                return col.get('column_id', '')
    return None

def load_papertable(filepath: str) -> List[Dict]:
    """Load papers from a papertable file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        papers = []
        if isinstance(data, dict) and 'data' in data and 'columns' in data:
            # Find the papers column
            papers_col_id = find_papers_column(data['columns'])
            
            if not papers_col_id:
                print(f"  Warning: Could not find papers column in {filepath}")
                return []
            
            # Extract papers from rows
            for row in data['data']:
                if isinstance(row, dict) and papers_col_id in row:
                    paper_data = row[papers_col_id]
                    if isinstance(paper_data, dict):
                        papers.append(paper_data)
        
        return papers
    except Exception as e:
        print(f"  Error loading {filepath}: {e}")
        return []

def save_papertable(papers: List[Dict], filepath: str):
    """Save papers to a papertable file."""
    # Create a simple column structure
    papers_col_id = "papers_deduplicated"
    
    # Create the data structure expected by papertable format
    rows = []
    for paper in papers:
        rows.append({papers_col_id: paper})
    
    data = {
        "columns": [
            {
                "column_id": papers_col_id,
                "name": f"Papers ({len(papers)})",
                "custom_instructions": None
            }
        ],
        "data": rows,
        "search_metadata": {
            "description": "Deduplicated papers from multiple searches"
        },
        "filter_info": {},
        "sort": None,
        "read_only": False,
        "disable_filters": False,
        "disable_sorting": False
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def deduplicate_papers(all_papers: List[Dict]) -> Tuple[List[Dict], int]:
    """
    Deduplicate papers using DOI, title, and author matching.
    Returns (unique_papers, duplicate_count)
    """
    unique_papers = []
    duplicate_count = 0
    
    print(f"  Starting deduplication of {len(all_papers)} papers...")
    
    for i, paper in enumerate(all_papers):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(all_papers)} papers...")
        
        is_duplicate = False
        
        # Check against all unique papers found so far
        for unique_paper in unique_papers:
            if are_duplicates(paper, unique_paper):
                is_duplicate = True
                duplicate_count += 1
                break
        
        if not is_duplicate:
            unique_papers.append(paper)
    
    print(f"  Deduplication complete: {len(unique_papers)} unique papers, {duplicate_count} duplicates removed")
    return unique_papers, duplicate_count

def main():
    workspace = "/home/sandbox"
    
    # List of all papertable files to process
    papertable_files = [
        # SciSpace
        "scispace_query_1.papertable",
        "scispace_query_2.papertable",
        "scispace_query_3.papertable",
        "scispace_query_4.papertable",
        "scispace_query_5.papertable",
        "scispace_query_6.papertable",
        # Google Scholar
        "google_scholar_query_1.papertable",
        "google_scholar_query_2.papertable",
        "google_scholar_query_3.papertable",
        "google_scholar_query_4.papertable",
        "google_scholar_query_5.papertable",
        "google_scholar_query_6.papertable",
        # ArXiv
        "arxiv_query_1.papertable",
        "arxiv_query_2.papertable",
        "arxiv_query_3.papertable",
        "arxiv_query_4.papertable",
        "arxiv_query_5.papertable",
        "arxiv_query_6.papertable",
    ]
    
    print("="*80)
    print("PAPER DEDUPLICATION PROCESS")
    print("="*80)
    
    # Load all papers from all files
    all_papers = []
    file_stats = {}
    
    print("\n1. Loading papers from all files...")
    for filename in papertable_files:
        filepath = os.path.join(workspace, filename)
        if os.path.exists(filepath):
            papers = load_papertable(filepath)
            file_stats[filename] = len(papers)
            all_papers.extend(papers)
            print(f"   ✓ {filename}: {len(papers)} papers")
        else:
            print(f"   ✗ {filename}: FILE NOT FOUND")
            file_stats[filename] = 0
    
    print(f"\n  Total papers loaded: {len(all_papers)}")
    
    if len(all_papers) == 0:
        print("\n  ERROR: No papers found in any file!")
        return
    
    # Deduplicate
    print("\n2. Performing deduplication...")
    unique_papers, duplicate_count = deduplicate_papers(all_papers)
    
    # Save results
    num_unique = len(unique_papers)
    output_filename = f"{num_unique}_papers_after_automated_deduplication.papertable"
    output_path = os.path.join(workspace, output_filename)
    
    print(f"\n3. Saving unique papers to {output_filename}...")
    save_papertable(unique_papers, output_path)
    
    # Generate summary report
    print("\n" + "="*80)
    print("DEDUPLICATION SUMMARY")
    print("="*80)
    print(f"\nTotal papers before deduplication: {len(all_papers)}")
    print(f"Unique papers after deduplication: {num_unique}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Deduplication rate: {(duplicate_count/len(all_papers)*100):.2f}%")
    
    print("\n" + "-"*80)
    print("Papers per source file (after year/type filtering):")
    print("-"*80)
    
    # Group by database
    scispace_total = sum(count for name, count in file_stats.items() if name.startswith('scispace'))
    scholar_total = sum(count for name, count in file_stats.items() if name.startswith('google_scholar'))
    arxiv_total = sum(count for name, count in file_stats.items() if name.startswith('arxiv'))
    
    print(f"\nSciSpace: {scispace_total} papers")
    for filename, count in file_stats.items():
        if filename.startswith('scispace'):
            print(f"  - {filename}: {count}")
    
    print(f"\nGoogle Scholar: {scholar_total} papers")
    for filename, count in file_stats.items():
        if filename.startswith('google_scholar'):
            print(f"  - {filename}: {count}")
    
    print(f"\nArXiv: {arxiv_total} papers")
    for filename, count in file_stats.items():
        if filename.startswith('arxiv'):
            print(f"  - {filename}: {count}")
    
    print("\n" + "="*80)
    print(f"✓ Output saved to: {output_filename}")
    print("="*80)
    
    # Save detailed statistics
    stats_file = os.path.join(workspace, "deduplication_statistics.json")
    stats = {
        "total_papers_before": len(all_papers),
        "unique_papers_after": num_unique,
        "duplicates_removed": duplicate_count,
        "deduplication_rate_percent": round(duplicate_count/len(all_papers)*100, 2),
        "database_totals": {
            "scispace": scispace_total,
            "google_scholar": scholar_total,
            "arxiv": arxiv_total
        },
        "file_statistics": file_stats,
        "output_file": output_filename,
        "filters_applied": {
            "year_range": "2019-2025",
            "publication_types": ["journal-article", "conference_paper", "report", "preprint"]
        }
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nDetailed statistics saved to: deduplication_statistics.json\n")

if __name__ == "__main__":
    main()
